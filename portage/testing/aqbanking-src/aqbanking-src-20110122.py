import os
from shells import MSysShell
import info
import utils


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.hardDependencies['testing/gwenhywfar-src'] = 'default'
        self.hardDependencies['win32libs-bin/mpir'] = 'default'
        if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'

    def setTargets( self ):
        self.targets['5.0.2'] = 'aqbanking-5.0.2.tar.gz'
        self.targetInstSrc['5.0.2'] = "aqbanking-5.0.2"

        self.options.package.withCompiler = False
        self.shortDescription = "Generic Online Banking Interface"
        self.defaultTarget = '5.0.2'

from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *
 
class PackageMinGW(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = "--enable-shared --disable-static"

    def fetch(self):
        utils.wgetFile('"http://www.aquamaniac.de/sites/download/download.php?package=03&release=75&file=01&dummy=aqbanking-5.0.2.tar.gz"' , self.downloadDir() , "aqbanking-5.0.2.tar.gz")
        return True

if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            self.subinfo = subinfo()
            VirtualPackageBase.__init__( self )

if __name__ == '__main__':
      Package().execute()
