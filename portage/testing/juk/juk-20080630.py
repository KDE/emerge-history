import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/KDE/kdemultimedia#norecursive;trunk/KDE/kdemultimedia/juk;trunk/KDE/kdemultimedia/cmake"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['win32libs-bin/taglib'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.configure.onlyBuildTargets = 'juk'
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()


