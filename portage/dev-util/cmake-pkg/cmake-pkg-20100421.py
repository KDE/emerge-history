# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://cmake.org/cmake.git"
        self.svnTargets['release'] = "git://cmake.org/cmake.git|release|"
        self.targets['2.8.1'] = "http://www.cmake.org/files/v2.8/cmake-2.8.1.tar.gz"
        self.targetInstSrc['2.8.1'] = "cmake-2.8.1"
        self.patchToApply['2.8.1'] = ("cmake-2.8.1-20100511.diff", 1)
        self.defaultTarget = 'release'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
if __name__ == '__main__':
    Package().execute()