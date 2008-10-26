import base
import os
import sys
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/graphics/kipi-plugins'
        self.targets['0.10.0-beta3'] = 'http://digikam3rdparty.free.fr/0.10.x-releases/kipi-plugins-0.2.0-beta3.tar.bz2'
        self.targetInstSrc['0.10.0-beta3'] = 'kipi-plugins-0.2.0-beta3'
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
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kipi-plugins", self.buildTarget, True )
        else:
            return self.doPackaging( "kipi-plugins", os.path.basename(sys.argv[0]).replace("kipi-plugins-", "").replace(".py", ""), True )


if __name__ == '__main__':		
    subclass().execute()
