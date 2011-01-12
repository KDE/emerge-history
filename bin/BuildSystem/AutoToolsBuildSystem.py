# -*- coding: utf-8 -*-
# definitions for the autotools build system

import os
import utils

import base
import info
import compiler
from shells import *

from BuildSystemBase import *

class AutoToolsBuildSystem(BuildSystemBase):
    def __init__( self ):
        self.buildInSource = False
        BuildSystemBase.__init__(self, "autotools", "AutoToolsBuildSystem")
        self.shell = MSysShell()
        self.makeProgram = "make -e"


    def configureDefaultDefines( self ):

        """defining the default cmake cmd line"""
        return ""

    def configure( self, cflags="", ldflags=""):
        """configure the target"""

        if self.buildInSource:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        if self.noCopy:
            sourcedir = self.sourceDir()
        else:
            sourcedir = self.buildDir()



        configure = os.path.join(sourcedir, "configure")
        if os.path.exists(configure) or self.subinfo.options.configure.bootstrap == True:
            mergeroot = self.shell.toNativePath( self.mergeDestinationDir() )
            _cflags = "-I%s/include %s" % (mergeroot, cflags)
            _ldflags = "-L%s/lib %s" % (mergeroot, ldflags)
            self.shell.initEnvironment(_cflags, _ldflags)
            if self.subinfo.options.configure.bootstrap == True:
                autogen = os.path.join(sourcedir, "autogen.sh")
                if os.path.exists(autogen):
                    self.shell.execute(self.sourceDir(), autogen, debugLvl=0)
            if self.subinfo.options.install.useDestDir == False:
                _prefix = "--prefix=" + self.shell.toNativePath(self.imageDir())
            else:
                _prefix = "--prefix=" + mergeroot
            _options = BuildSystemBase.configureOptions(self)
            if _options:
                _prefix += " %s" % _options
            if self.buildInSource:
                ret = self.shell.execute(self.sourceDir(), configure, _prefix, debugLvl=0 )
            else:
                ret = self.shell.execute(self.buildDir(), configure, _prefix, debugLvl=0  )
        else:
            ret = self.shell.execute(self.sourceDir(), "ruby", "configure", debugLvl=0 )
        return ret

    def make( self, buildType=None ):
        """Using the *make program"""
        if self.buildInSource:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        command = self.makeProgram
        args = ""
        if self.subinfo.options.make.ignoreErrors:
            args += " -i"

        if self.subinfo.options.make.makeOptions:
            args += " %s" % self.subinfo.options.make.makeOptions

        # adding Targets later
        if utils.verbose() > 1:
            args += " VERBOSE=1"
        if self.buildInSource:
            self.shell.execute(self.sourceDir(), command, args ) or utils.die( "while Make'ing. cmd: %s" % command )
        else:
            self.shell.execute(self.buildDir(), command, args ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def install( self ):
        """Using *make install"""

        if self.buildInSource:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        command = self.makeProgram
        args = "install"

        if self.subinfo.options.install.useDestDir == True:
            args += " DESTDIR=%s prefix=." % self.shell.toNativePath( self.installDir() )

        if self.subinfo.options.make.ignoreErrors:
            args += " -i"

        if self.subinfo.options.make.makeOptions:
            args += " %s" % self.subinfo.options.make.makeOptions
        if self.buildInSource:
            return self.shell.execute(self.sourceDir(), command, args) or utils.die( "while installing. cmd: %s %s" % (command, args) )
        else:
            return self.shell.execute(self.buildDir(), command, args) or utils.die( "while installing. cmd: %s %s" % (command, args) )

    def runTest( self ):
        """running unittests"""
        return true

    def createShell( self ):
        """create shell in package build dir with prepared environment"""

        if self.buildInSource:
            self.enterSourceDir()
            self.shell.openShell(self.sourceDir())
        else:
            self.enterBuildDir()
            self.shell.openShell(self.buildDir())
        return True


