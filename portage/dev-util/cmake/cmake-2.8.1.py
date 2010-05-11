import info
import platform

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['2.4.8'] = 'http://www.cmake.org/files/v2.4/cmake-2.4.8-win32-x86.zip'
        self.targets['2.6.4'] = 'http://www.cmake.org/files/v2.6/cmake-2.6.4-win32-x86.zip'
        self.targets['2.8.0'] = 'http://www.cmake.org/files/v2.8/cmake-2.8.0-win32-x86.zip'
        self.targets['2.8.1'] = 'http://www.cmake.org/files/v2.8/cmake-2.8.1-win32-x86.zip'
        self.targets['2.8.0-ce'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-2.8.0-bin.tar.bz2'
        self.targets['2.8.1-ce'] = 'http://downloads.sourceforge.net/kde-windows/cmake-vc90-2.8.1-bin.tar.bz2'
        self.targetMergeSourcePath['2.4.8'] = 'cmake-2.4.8-win32-x86'
        self.targetMergeSourcePath['2.6.4'] = 'cmake-2.6.4-win32-x86'
        self.targetMergeSourcePath['2.8.0'] = 'cmake-2.8.0-win32-x86'
        self.targetMergeSourcePath['2.8.1'] = 'cmake-2.8.1-win32-x86'

        self.patchToApply['2.8.0'] = ('cmake-2.8.0-wince-support.patch', 0)

        if platform.isCrossCompilingEnabled():
            self.defaultTarget = '2.8.0-ce'
        else:
            self.defaultTarget = '2.8.1'
            
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
