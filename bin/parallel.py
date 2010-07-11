#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copyright 2010 by Intevation GmbH
#
"""Tool to use emerge in 'make -k' and 'make -j' way.

   When emerging a more complex package depending on several
   sub packages it is likely that emerge dies for some reasons 
   at different parts of process. Without this tool you are
   forced to fix the detected problem one after the other
   and start the emerging again and again.

   The 'emerge -k' does not stop at the first error and
   builds as much as its possible to generate a maximal
   error report.

   In the dependency graph of an emerge target some parts
   are independent from each other so it is possible to
   build them parallel. This goes beyond a classical 'make -j'
   because having this feature at emerge level you are
   able get fetch sources of one package and compile another.

   Usage:

   Preconditon: Set the environment variables used by emerge.

   $ python bin/parallel.py -j <# workers> -c <command>

   with <# workers> is the number of parallel running jobs.
   Defaults to the number of processor cores of the machine.

   <command> is template for the command to be executed
   for each sub package. Defaults to:
   'python emerge.py %(category)s/%(package)s'

   category, package, version and tag are subsituted
   in the command string before being executed.
"""

__author__  = "Sascha L. Teichmann <sascha.teichmann@intevation.de>"
__license__ = "GNU General Public License (GPL)"

import getopt
import os.path
import sys
import traceback

from datetime import datetime

from multiprocessing import Process, Queue, cpu_count

import portage

import utils

from dependencies import DependenciesTree


DEFAULT_COMMAND = "python %s %%(category)s/%%(package)s" % \
    os.path.join(os.getenv("KDEROOT", os.curdir), "bin", "emerge.py")


def now():
    """Returns current timestamp as string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(kind, msg):
    """Writes timestamped message"""
    print "builder: %s %s %s" % (now(), kind, msg)
    sys.stdout.flush()

class Job(object):
    """An emerge work job.
       References a node in the dependency graph to access the
       informations to generate a concrete emerge call.
       The number of blocking jobs is also tracked. If this
       number goes down to zero this job is ready for execution.
       Error codes are propagated through the calling jobs chains.
    """

    def __init__(self, node):
        """Creates a new emerge job for given node in the dependency graph."""
        self.node      = node
        self.dep_count = len(node.children)
        self.dep_exit  = 0

    def create_command(self, command):
        """Fills the given command template with information from the
           corresponding node in the dependency graph.
        """
        node = self.node
        return command % {
            'category': node.category,
            'package' : node.package,
            'version' : node.version,
            'tag'     : node.tag }

    def unblock(self, dep_exit):
        """Decreases the count of blocking jobs which need to be
           processed before this job is ready for execution.
           Error codes are stored to be propagated through the
           graph waiting for this job.
           Returns true if this job is ready for execution.
        """
        if dep_exit != 0: self.dep_exit = dep_exit
        self.dep_count -= 1
        return self.dep_count < 1

    def trigger_exec(self, command):
        """Generates a tuple to enable the workers to execute this job."""
        if self.dep_exit != 0:
            # propagate error
            return (str(self.node), "", self.dep_exit)
        else:
            return (str(self.node), self.create_command(command))

class Worker(Process):
    """An asynchronous working job executor.
       It takes its jobs from a 'todo' queue
       and puts the results to a 'done' queue.
    """

    def __init__(self, todo, done):
        """Creates a worker with a 'todo' and a 'done' job queue.""" 
        Process.__init__(self)
        self.todo   = todo
        self.done   = done
        self.daemon = True
        self.start()

    def run(self):
        """Takes jobs from the 'todo' queue, processes them
           and puts the results into the 'done' queue.
        """
        while True:
            execute = self.todo.get()
            if len(execute) > 2:
                # propagate error
                self.done.put((execute[0], execute[2]))
            else:
                log("start", execute[0])
                sys.stdout.flush()
                exit_code = 1
                try:
                    exit_code = os.system(execute[1])
                except:
                    traceback.print_exc()
                log("stop", execute[0])
                sys.stdout.flush()
                self.done.put((execute[0], exit_code))

class ParallelBuilder(object):
    """Converts a dependency graph into lists of jobs to be executed
       in a botton up manner. Independent jobs are processed
       in parallel with a given number of workers.
    """

    def __init__(self, command):
        """Creates a builder with a given command template."""
        self.command = command

    def build_blocked(self, node, blocked, jobs, ready):
        """Recursive working method to create the jobs lists from the
           dependency tree.
        """
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
        """Builds a dependency tree with a number of workers.
           If no explicit number of workers is given the
           number of processor cores is used.
        """

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
            todo.put(job.trigger_exec(self.command))

        ready = None

        jobs_left = len(jobs)

        final_exit_code = 0

        while jobs_left:
            key, exit_code = done.get()

            if exit_code != 0: final_exit_code = exit_code

            try:
                blocked_list = blocked.pop(key)
            except KeyError:
                break

            for job in blocked_list:
                if job.unblock(exit_code):
                    todo.put(job.trigger_exec(self.command))

            jobs_left -= 1

        return final_exit_code

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
    
    log("start", "all")
    exit_code = builder.build(dep_tree, num_worker)
    log("stop", "all")

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
