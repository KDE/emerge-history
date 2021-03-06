import info

from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.3.1'] = 'http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.1.tar.gz'
        self.targetInstSrc['1.3.1'] = 'libvorbis-1.3.1'
        self.patchToApply['1.3.1'] = ( 'libvorbis-1.3.1-20100708.diff', 1 )
        self.targetDigests['1.3.1'] = '0874dd08699240b868b22979da4c95ae6325006b'
        self.shortDescription = "reference implementation for the vorbis video file format"
        self.defaultTarget = '1.3.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/libogg'] = 'default'

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
