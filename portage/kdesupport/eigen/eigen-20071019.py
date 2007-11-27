import base
import utils
from utils import die
import os
import sys

DEPEND = """
virtual/base
"""

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        # header-only package
        self.createCombinedPackage = True
        self.instsrcdir = "eigen"

    def kdeSvnPath( self ):
        return "trunk/kdesupport/eigen"

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.traditional:
            self.instdestdir = "kde"
        return self.doPackaging( "eigen", os.path.basename(sys.argv[0]).replace("eigen-", "").replace(".py", ""), True )        

subclass().execute()
