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
        self.instsrcdir = "kdegraphics"
        if self.traditional:
            self.instdestdir = "kde"

    def kdeSvnPath( self ):
        return "trunk/KDE/kdegraphics"

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        if self.compiler == "mingw":
            self.kdeCustomDefines = "-DBUILD_kolourpaint=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdegraphics", os.path.basename(sys.argv[0]).replace("kdegraphics-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
