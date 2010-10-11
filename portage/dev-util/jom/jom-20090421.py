# -*- coding: utf-8 -*-
import base
import info
import shutil
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

    def setTargets( self ):
        self.targets['HEAD'] = 'ftp://ftp.qt.nokia.com/jom/jom.zip'
        self.targets['094'] = 'ftp://ftp.qt.nokia.com/jom/jom094.zip'
        self.targetDigests['094'] = '1f946283866cd6f40a5888088f6c7d840b62af2d'
        self.targetInstallPath['094'] = "bin"
        self.targetInstallPath['HEAD'] = "bin"
        self.defaultTarget = '094'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
