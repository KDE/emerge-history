import base

DEPEND = """
virtual/base
"""

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )

    def kdeSvnPath( self ):
        return "trunk/kdesupport/kdewin32"

    def unpack( self ):
        return self.kdeSvnUnpack( "trunk/kdesupport", "kdewin32" )

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.traditional:
            self.instdestdir = "kde"
            self.instsrcdir = "kdewin32"
        return self.doPackaging( "kdewin32", "0.3.1-1", True )

subclass().execute()
