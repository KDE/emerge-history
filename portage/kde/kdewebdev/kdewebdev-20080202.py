import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdewebdev'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdewebdev'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdewebdev-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdewebdev-4.0.60'
        self.targets['4.0.61'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.61/src/kdewebdev-4.0.61.tar.bz2'
        self.targetInstSrc['4.0.61'] = 'kdewebdev-4.0.61'
        self.targets['4.0.62'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.62/src/kdewebdev-4.0.62.tar.bz2'
        self.targetInstSrc['4.0.62'] = 'kdewebdev-4.0.62'
        self.targets['4.0.63'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.63/src/kdewebdev-4.0.63.tar.bz2'
        self.targetInstSrc['4.0.63'] = 'kdewebdev-4.0.63'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.softDependencies['kde/kdevplatform'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        # if you want to build quanta, you need to build kdevplatform as well - this is not build by default!!!
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_quanta=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kfilereplace=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kxsldbg=OFF "

        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdewebdev", self.buildTarget, True )
        else:
            return self.doPackaging( "kdewebdev", os.path.basename(sys.argv[0]).replace("kdewebdev-", "").replace(".py", ""), True )


if __name__ == '__main__':
    subclass().execute()
