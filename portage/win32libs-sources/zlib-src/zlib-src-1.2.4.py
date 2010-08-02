# -*- coding: utf-8 -*-
import info
import utils
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
       for ver in [ '1.2.4' ]:
           self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/libpng/zlib-%s.tar.gz' % ver
           self.targetInstSrc[ ver ] = "zlib-" + ver
       self.patchToApply['1.2.4'] = ("zlib-1.2.4-20100422.diff", 1)
       self.defaultTarget = '1.2.4'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        if platform.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-sources/wcecompat-src'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def unpack(self):
        if not CMakePackageBase.unpack( self ):
            return False       
        if os.path.exists(os.path.join( self.sourceDir() , "zconf.h" )):
            os.remove(os.path.join( self.sourceDir() , "zconf.h" ))
        return True

    def createPackage( self ):
        # auto-create both import libs with the help of pexports
        self.createImportLibs( "libzlib1" )

        return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
