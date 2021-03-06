import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.2/kdeedu'
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.2.' + ver + '/src/kdeedu-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdeedu-4.2.' + ver
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde-4.2/kdebase-runtime'] = 'default'

        self.softDependencies['kdesupport/eigen'] = 'default'
        self.softDependencies['kdesupport/gmm'] = 'default'
        self.hardDependencies['win32libs-bin/cfitsio'] = 'default'
        self.hardDependencies['win32libs-bin/libnova'] = 'default'
        self.hardDependencies['win32libs-bin/openbabel'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdeedu"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DBUILD_doc=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdeedu", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
