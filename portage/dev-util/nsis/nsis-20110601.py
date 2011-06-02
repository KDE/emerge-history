import info
import os
import shutil

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setTargets( self ):
        self.targets['2.46'] = 'http://downloads.sourceforge.net/sourceforge/nsis/nsis-2.46.zip'
        self.targetDigests['2.46'] = 'adeff823a1f8af3c19783700a6b8d9054cf0f3c2'
        self.defaultTarget = '2.46'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = os.path.join("dev-utils")
        BinaryPackageBase.__init__(self)

    def unpack( self ):
        if not BinaryPackageBase.unpack(self):
            return False
        localFileDir = self.localFileNames()[0].replace(".zip", "")
        for f in os.listdir(os.path.join(self.imageDir(), localFileDir)):
            shutil.move(os.path.join(self.imageDir(), localFileDir, f), self.imageDir())
        os.rmdir(os.path.join(self.imageDir(), localFileDir))
        for f in ['makensis', 'makensisw', 'nsis']:
            shutil.copy(os.path.join(self.packageDir(), "wrapper.bat"), os.path.join(self.imageDir(), "bin", f + ".bat"))
        return True

if __name__ == '__main__':
    Package().execute()
