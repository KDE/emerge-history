import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/automoc'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "automoc"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            return self.doPackaging( "automoc", os.path.basename(sys.argv[0]).replace("automoc-", ""), True )
        else:
            return self.doPackaging( "automoc", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
