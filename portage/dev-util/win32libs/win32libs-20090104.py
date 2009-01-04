import base
import os
import utils
import shutil
import info

SRC_URI= """
http://downloads.sourceforge.net/kde-windows/aspell-0.60.5-bin.zip
http://downloads.sourceforge.net/kde-windows/aspell-0.60.5-lib.zip

http://downloads.sourceforge.net/kde-windows/libbzip2-1.0.5-1-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/libbzip2-1.0.5-1-lib.tar.bz2

http://downloads.sourceforge.net/kde-windows/expat-2.0.1-bin.zip
http://downloads.sourceforge.net/kde-windows/expat-2.0.1-lib.zip

http://downloads.sourceforge.net/kde-windows/gettext-0.17-1-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/gettext-0.17-1-lib.tar.bz2

http://downloads.sourceforge.net/kde-windows/giflib-4.1.4-1-bin.zip
http://downloads.sourceforge.net/kde-windows/giflib-4.1.4-1-lib.zip

http://downloads.sourceforge.net/kde-windows/gpgme-1.1.4-3-bin.zip
http://downloads.sourceforge.net/kde-windows/gpgme-1.1.4-3-lib.zip

http://downloads.sourceforge.net/kde-windows/iconv-1.9.2-2-bin.zip
http://downloads.sourceforge.net/kde-windows/iconv-1.9.2-2-lib.zip

http://downloads.sourceforge.net/kde-windows/jasper-1.900.1-2-bin.zip
http://downloads.sourceforge.net/kde-windows/jasper-1.900.1-2-lib.zip

http://downloads.sourceforge.net/kde-windows/jpeg-6.b-5-bin.zip
http://downloads.sourceforge.net/kde-windows/jpeg-6.b-5-lib.zip

http://downloads.sourceforge.net/kde-windows/lcms-1.17-bin.zip
http://downloads.sourceforge.net/kde-windows/lcms-1.17-lib.zip

http://downloads.sourceforge.net/kde-windows/libical-0.42-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/libical-0.42-lib.tar.bz2

http://downloads.sourceforge.net/kde-windows/libidn-1.2-1-bin.zip
http://downloads.sourceforge.net/kde-windows/libidn-1.2-1-lib.zip

http://downloads.sourceforge.net/kde-windows/libpng-1.2.29-1-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/libpng-1.2.29-1-lib.tar.bz2

http://downloads.sourceforge.net/kde-windows/libxml2-2.6.30-3-bin.zip
http://downloads.sourceforge.net/kde-windows/libxml2-2.6.30-3-lib.zip

http://downloads.sourceforge.net/kde-windows/libxslt-1.1.23-3-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/libxslt-1.1.23-3-lib.tar.bz2

http://downloads.sourceforge.net/kde-windows/openslp-1.2.1-2-bin.zip
http://downloads.sourceforge.net/kde-windows/openslp-1.2.1-2-lib.zip

http://downloads.sourceforge.net/kde-windows/openssl-0.9.8g-1-bin.zip
http://downloads.sourceforge.net/kde-windows/openssl-0.9.8g-1-lib.zip

http://downloads.sourceforge.net/kde-windows/redland-1.0.3-5-bin.zip
http://downloads.sourceforge.net/kde-windows/redland-1.0.3-5-lib.zip

http://downloads.sourceforge.net/kde-windows/shared-mime-info-0.51-1-bin.tar.bz2

http://downloads.sourceforge.net/kde-windows/tiff-3.8.2-2-bin.zip
http://downloads.sourceforge.net/kde-windows/tiff-3.8.2-2-lib.zip

http://downloads.sourceforge.net/kde-windows/zlib-1.2.3-2-bin.zip
http://downloads.sourceforge.net/kde-windows/zlib-1.2.3-2-lib.zip

http://downloads.sourceforge.net/sourceforge/gnuwin32/zip-2.31-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/zip-2.31-lib.zip
"""

if os.getenv("KDECOMPILER") == "mingw":
    SRC_URI = SRC_URI + """
http://downloads.sourceforge.net/kde-windows/boost-mingw-1.37.0-1-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/boost-mingw-1.37.0-1-lib.tar.bz2

http://downloads.sourceforge.net/kde-windows/dbus-mingw-1.2.4-1-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/dbus-mingw-1.2.4-1-lib.tar.bz2

http://downloads.sourceforge.net/kde-windows/pcre-mingw-7.8-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/pcre-mingw-7.8-lib.tar.bz2
"""
else:
    SRC_URI = SRC_URI + """
http://downloads.sourceforge.net/kde-windows/boost-msvc-1.37.0-1-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/boost-msvc-1.37.0-1-lib.tar.bz2

http://downloads.sourceforge.net/kde-windows/dbus-msvc-1.2.4-1-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/dbus-msvc-1.2.4-1-lib.tar.bz2

http://downloads.sourceforge.net/kde-windows/pcre-msvc-7.8-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/pcre-msvc-7.8-lib.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['HEAD'] = SRC_URI
        self.defaultTarget = 'HEAD'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    if self.traditional:
        self.instdestdir = "win32libs"
    else:
        self.instdestdir = ""
    self.subinfo = subinfo()

  def compile(self):
    if self.compiler == "mingw":
        srcfile = os.path.join( self.workdir, "lib", "libdbus-1.dll.a" )
        destfile = os.path.join( self.workdir, "lib", "libdbus-1d.dll.a" )
        shutil.copy( srcfile, destfile )
        srcfile = os.path.join( self.workdir, "bin", "libdbus-1.dll" )
        destfile = os.path.join( self.workdir, "bin", "libdbus-1d.dll" )
        shutil.copy( srcfile, destfile )

    return True

if __name__ == '__main__':
    subclass().execute()
