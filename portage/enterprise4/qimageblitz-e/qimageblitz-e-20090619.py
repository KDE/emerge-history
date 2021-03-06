import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['enterprise4/qt-e'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.0.5'] = 'tags/qimageblitz/0.0.5'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qimageblitz'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "qimageblitz"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "qimageblitz", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
