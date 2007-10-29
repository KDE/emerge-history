import base
import os
import shutil
import utils

PACKAGE_NAME         = "libiconv"
PACKAGE_VER          = "1.9.2"
PACKAGE_FULL_VER     = "1.9.2-2"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAMES    = """
libiconv2
libcharset1
"""

SRC_URI= """
http://heanet.dl.sourceforge.net/sourceforge/gnuwin32/libiconv-1.9.2-1.exe
"""

DEPEND = """
"""

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    self.createCombinedPackage = True

  def unpack( self ):

    # hopefully only one...
    for filename in self.filenames:
        os.system( os.path.join( self.downloaddir, filename ) + " /DIR=\"" + self.workdir + "\" /SILENT")

    return True

  def compile( self ):
    # binary-only package - nothing to compile
    return True

  def install( self ):
    # cleanup
    dst = os.path.join( self.imagedir )
    utils.cleanDirectory( dst )
    dst = os.path.join( self.imagedir, self.instdestdir )
    utils.cleanDirectory( dst )

    # /bin only contains zlib1.dll
    dst = os.path.join( self.imagedir, self.instdestdir, "bin" )
    utils.cleanDirectory( dst )

    for libs in PACKAGE_DLL_NAMES.split():
        src = os.path.join( self.workdir, self.instsrcdir, "bin", libs + ".dll" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", libs + ".dll" )
        shutil.copy( src, dst )

    # /contrib/PACKAGE_NAME/PACKAGE_FULL_VER
    src = os.path.join( self.workdir, self.instsrcdir, "contrib" )
    dst = os.path.join( self.imagedir, self.instdestdir, "contrib" )
    utils.copySrcDirToDestDir( src, dst )

    # /include can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "include" )
    dst = os.path.join( self.imagedir, self.instdestdir, "include" )
    utils.copySrcDirToDestDir( src, dst )

    # /lib needs a complete rebuild - done in make_package
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )

    return True
  def make_package( self ):
    self.instsrcdir = ""

    # auto-create both import libs with the help of pexports
    for libs in PACKAGE_DLL_NAMES.split():
        self.createImportLibs( libs )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

    return True
  
subclass().execute()
