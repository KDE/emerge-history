# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['2.3.7-2']:
            self.targets[ version ] = self.getPackage( repoUrl, "freetype", version )

        self.defaultTarget = '2.3.7-2'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True


class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
