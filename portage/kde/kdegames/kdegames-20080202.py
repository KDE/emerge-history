import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdegames'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdegames'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdegames-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdegames-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        self.kdeSvnUnpack()
        return True

    def compile( self ):
        self.kdeCustomDefines = ""
#        self.kdeCustomDefines += " -DBUILD_doc=OFF"
#        self.kdeCustomDefines += " -DBUILD_bovo=OFF"
#        self.kdeCustomDefines += " -DBUILD_lskat=OFF"
#        self.kdeCustomDefines += " -DBUILD_katomic=OFF"
#        self.kdeCustomDefines += " -DBUILD_kbattleship=OFF"
#        self.kdeCustomDefines += " -DBUILD_kblackbox=OFF"
#        self.kdeCustomDefines += " -DBUILD_kblocks=OFF"
#        self.kdeCustomDefines += " -DBUILD_kbounce=OFF"
#        self.kdeCustomDefines += " -DBUILD_kbreakout=OFF"
#        self.kdeCustomDefines += " -DBUILD_kdiamond=OFF"
#        self.kdeCustomDefines += " -DBUILD_kfourinline=OFF"
#        self.kdeCustomDefines += " -DBUILD_kgoldrunner=OFF"
#        self.kdeCustomDefines += " -DBUILD_kiriki=OFF"
#        self.kdeCustomDefines += " -DBUILD_kjumpingcube=OFF"
#        self.kdeCustomDefines += " -DBUILD_klines=OFF"
#        self.kdeCustomDefines += " -DBUILD_kmahjongg=OFF"
#        self.kdeCustomDefines += " -DBUILD_kmines=OFF"
#        self.kdeCustomDefines += " -DBUILD_knetwalk=OFF"
#        self.kdeCustomDefines += " -DBUILD_kolf=OFF"
#        self.kdeCustomDefines += " -DBUILD_kollision=OFF"
#        self.kdeCustomDefines += " -DBUILD_konquest=OFF"
#        self.kdeCustomDefines += " -DBUILD_kpat=OFF"
#        self.kdeCustomDefines += " -DBUILD_kreversi=OFF"
#        self.kdeCustomDefines += " -DBUILD_ksame=OFF"
#        self.kdeCustomDefines += " -DBUILD_kshisen=OFF"
#        self.kdeCustomDefines += " -DBUILD_ksirk=OFF"
#        self.kdeCustomDefines += " -DBUILD_kspaceduel=OFF"
#        self.kdeCustomDefines += " -DBUILD_ksquares=OFF"
#        self.kdeCustomDefines += " -DBUILD_ktuberling=OFF"
#        self.kdeCustomDefines += " -DBUILD_ksudoku=OFF"
#        self.kdeCustomDefines += " -DBUILD_kubrick=OFF"
        return self.kdeCompile()
    
    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdegames", self.buildTarget, True )
        else:
            return self.doPackaging( "kdegames" )

if __name__ == '__main__':
    subclass().execute()
