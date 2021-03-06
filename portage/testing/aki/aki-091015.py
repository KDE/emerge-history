import base
import utils
import os
import sys
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/playground/network/aki'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['testing/akiirc'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "aki", self.buildTarget, True )
        else:
            return self.doPackaging( "aki", os.path.basename(sys.argv[0]).replace("aki-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()