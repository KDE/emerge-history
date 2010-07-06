#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copyright 2010 by Intevation GmbH

__author__  = "Sascha L. Teichmann <sascha.teichmann@intevation.de>"
__license__ = "GNU General Public License (GPL)"

import getopt
import os.path
import sys
import traceback

import portage

import utils

from dependencies import DependenciesTree

from multiprocessing import Process, Queue, cpu_count

DEFAULT_COMMAND = "python %s %%(category)s/%%(package)s" % \
    os.path.join(os.getenv("KDEROOT", os.curdir), "bin", "emerge.py")

class Job(object):

    def __init__(self, node):
        self.node      = node
        self.dep_count = len(node.children)
        self.dep_exit  = 0

    def create_command(self, command):
        node = self.node
        return command % {
            'category': node.category,
            'package' : node.package,
            'version' : node.version,
            'tag'     : node.tag }

    def unblock(self, dep_exit):
        if dep_exit != 0: self.dep_exit = dep_exit
        self.dep_count -= 1
        return self.dep_count < 1

    def key(self):
        return str(self.node)

    def is_buildable(self):
        return self.dep_exit == 0

    def transfer(self, command):
        return (str(self.node), self.create_command(command))


class Worker(Process):

    def __init__(self, todo, done):
        Process.__init__(self)
        self.todo   = todo
        self.done   = done
        self.daemon = True
        self.start()

    def run(self):
        while True:
            (key, command) = self.todo.get()
            exit_code = 1
            try:
                exit_code = os.system(command)
            except:
                traceback.print_exc()
            self.done.put((key, exit_code))

class ParallelBuilder(object):

    def __init__(self, command):
        self.command = command

    def build_blocked(self, node, blocked, jobs, ready):
        key = str(node)
        try:
            return jobs[key]
        except KeyError:
            pass

        job = Job(node)
        jobs[key] = job

        if node.children:
            for child in node.children:
                self.build_blocked(child, blocked, jobs, ready)
                block_list = blocked.setdefault(str(child), [])
                block_list.append(job)
        else:
            ready.add(job)

        return job

    def build(self, dep_tree, num_worker = None):

        if num_worker is None: num_worker = cpu_count()

        utils.debug("worker: %d" % num_worker)

        jobs, blocked, ready = {}, {}, set()

        for root in dep_tree.roots:
            self.build_blocked(root, blocked, jobs, ready)

        utils.debug("jobs: %d" % len(jobs))
        utils.debug("blocked: %d" % len(blocked))
        utils.debug("ready: %d" % len(ready))

        todo, done = Queue(), Queue()

        for _ in range(num_worker): Worker(todo, done)

        for job in ready:
            todo.put(job.transfer(self.command))

        ready = None

        jobs_left = len(jobs)

        while jobs_left:
            key, exit_code = done.get()

            try:
                blocked_list = blocked.pop(key)
            except KeyError:
                break

            for job in blocked_list:
                if job.unblock(exit_code) and job.is_buildable():
                    todo.put(job.transfer(self.command))

            jobs_left -= 1

def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "c:j:", ["command=", "jobs="])
    except getopt.GetoptError, err:
        print >> sys.stderr, str(err)
        sys.exit(1)

    if len(args) < 1:
        print >> sys.stderr, "missing package"
        sys.exit(1)

    command = DEFAULT_COMMAND

    num_worker = None

    for o, a in opts:
        if o in ("-c", "--command"):
            command = a
        elif o in ("-j", "--jobs"):
            num_worker = max(1, int(a))

    packageList, categoryList = portage.get_packages_categories(args[0])

    dep_tree = DependenciesTree()

    for category, package in zip(categoryList, packageList):
        dep_tree.add_dependencies(category, package)

    builder = ParallelBuilder(command)

    builder.build(dep_tree, num_worker)

if __name__ == '__main__':
    main()
