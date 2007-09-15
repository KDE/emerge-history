import base
import os
import shutil
import utils
from utils import die

PACKAGE_NAME         = "aspell"
PACKAGE_VER          = "0.60.5"
PACKAGE_FULL_VER     = "0.60.5"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAMES     = """
libaspell-15
libpspell-15
"""

SRC_URI= """
ftp://ftp.gnu.org/gnu/aspell/""" + PACKAGE_FULL_NAME + """.tar.gz
"""

DEPEND = """
dev-util/win32libs
"""

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    self.instsrcdir = PACKAGE_FULL_NAME
    self.createCombinedPackage = True

  def unpack( self ):
    if( not base.baseclass.unpack( self ) ):
      return False

    src = os.path.join( self.workdir, self.instsrcdir )
    cmd = "cd %s && patch -p0 < %s" % \
          ( src, os.path.join( self.packagedir , "aspell-0.60.5.diff" ) )
    os.system( cmd ) or die
    return True

  def compile( self ):
    incdir = os.path.join( self.rootdir, "win32libs", "include" )
    libdir = os.path.join( self.rootdir, "win32libs", "lib" )
    # fixme: libiconv is a dependency...
    os.environ[ "LDFLAGS" ] = "-L" + utils.toMSysPath( libdir )
    os.environ[ "CFLAGS" ]  = "-I" + utils.toMSysPath( incdir )
    return self.msysCompile( False )

  def install( self ):
    return self.msysInstall( False )

  def make_package( self ):
    for libs in PACKAGE_DLL_NAMES.split():
        self.stripLibs( libs )

    # auto-create both import libs with the help of pexports
    # one problem here - aspell has also a c++ interface which can't be used...
    # -> remove those functions from the export libs
    for libs in PACKAGE_DLL_NAMES.split():
        self.createImportLibs( libs )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

    return True
  
subclass().execute()
