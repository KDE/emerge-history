import os
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.19'] = "http://download.sourceforge.net/lcms/lcms-1.19.tar.gz"
        self.targetInstSrc['1.19'] = "lcms-1.19"
        self.patchToApply['1.19'] = ( 'lcms-1.19-20100416.diff', 1 )
        self.defaultTarget = '1.19'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        # both examples and tests can be run here
        self.subinfo.options.configure.defines = "-DBUILD_TESTS=OFF -DBUILD_SAMPLES=ON -DBUILD_TOOLS=OFF"
        self.subinfo.options.package.withCompiler = None

if __name__ == '__main__':
    Package().execute()
