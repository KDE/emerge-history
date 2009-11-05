# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091103'] = 'tags/kdepim/pe5.20091103/kdepim'
        self.defaultTarget = '20091103'

    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdebase-runtime'] = 'default'
        self.hardDependencies['enterprise5/kdepimlibs'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON"
        #        self.subinfo.options.configure.defines += " -DBUILD_doc=OFF"

if __name__ == '__main__':
    Package().execute()

