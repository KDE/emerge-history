# -*- coding: utf-8 -*-
import utils
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://github.com/kromain/wcecompat.git|komo3|'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.packageName = 'wcecompat'
        self.subinfo.options.configure.defines = "-DWCECOMPAT_INSTALL_INC_DIR=include/wcecompat"

if __name__ == '__main__':
    Package().execute()
