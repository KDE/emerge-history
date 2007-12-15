import base
import os
import sys

DEPEND = """
kde/kdelibs
kde/kdepimlibs
"""

class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "kdebase"

    def kdeSvnPath( self ):
        return "trunk/KDE/kdebase"
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdebase", os.path.basename(sys.argv[0]).replace("kdebase-", "").replace(".py", ""), True )

		
subclass().execute()
