# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for ver in ['0.10.3', '0.10.4', '0.10.5', '0.10.6']:
            self.targets[ ver ] = self.getPackage( repoUrl, "poppler", ver )

        self.defaultTarget = '0.10.6'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        self.hardDependencies['win32libs-bin/openjpeg'] = 'default'
        self.hardDependencies['win32libs-bin/lcms'] = 'default'
        self.hardDependencies['data/poppler-data'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
