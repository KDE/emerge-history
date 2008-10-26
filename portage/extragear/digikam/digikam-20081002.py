import base
import os
import sys
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/graphics/digikam'
        self.target['0.10.0-beta5'] = 'http://digikam3rdparty.free.fr/0.10.x-releases/digikam-0.10.0-beta5.tar.bz2'
        self.targetInstSrc['0.10.0-beta5'] = 'digikam-0.10.0-beta5'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdegraphics'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "digikam"
        self.subinfo = subinfo()

    def unpack( self ):
        if self.buildTarget == '0.10.0-beta5'
            if( not base.baseclass.unpack( self ) ):
                return True
            else:
                return False
        else:
            return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DENABLE_GPHOTO2=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "digikam", self.buildTarget, True )
        else:
            return self.doPackaging( "digikam", os.path.basename(sys.argv[0]).replace("digikam-", "").replace(".py", ""), True )


if __name__ == '__main__':		
    subclass().execute()
