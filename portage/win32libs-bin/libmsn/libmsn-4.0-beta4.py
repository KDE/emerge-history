# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['4.0-beta2', '4.0-beta4']:
            self.targets[ version ] = self.getPackage( repoUrl, "libmsn", version )

        self.defaultTarget = '4.0-beta4'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
