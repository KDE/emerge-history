import base
import utils
import os
import sys

DEPEND = """
kde/kdebase
"""

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "kdesdk"

    def kdeSvnPath( self ):
        return "trunk/KDE/kdesdk"
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdesdk", os.path.basename(sys.argv[0]).replace("kdesdk-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
