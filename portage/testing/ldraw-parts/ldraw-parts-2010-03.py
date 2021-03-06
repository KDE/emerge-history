import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '2010-03' ] =  "http://www.ldraw.org/library/updates/complete.zip"
        self.targetDigests['2010-03'] = 'b6b2cc3445198632e4017c63027ec4732a2de4f2'
        self.shortDescription = 'LDraw Parts Library'
        self.defaultTarget = '2010-03'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        self.subinfo.options.install.installPath = "share"

if __name__ == '__main__':
    Package().execute()
