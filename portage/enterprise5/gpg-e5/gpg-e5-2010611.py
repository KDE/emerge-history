# GnuPG - Windows development package
#
# This Package contains the headers and libraries for the gnupg software:
# 
# libgpg-error-1.8
# libgcrypt-1.4.5
# libassuan-2.0.0
# libksba-1.0.7
# gpgme-1.3.0
#
# The intention is that they should keep up with the recent versions of gpg4win
# (www.gpg4win.de) which packages gnupg seperatly so KDE software can interact
# with gpg4win.

from Package.BinaryPackageBase import *
import os
import info
import glob

class subinfo(info.infoclass):

    def setTargets( self ):
        version="20100611"
        self.targets[version] = \
            "ftp://ftp.gnupg.org/gcrypt/binary/gpg-w32-dev-"+version+".zip"
        self.defaultTarget = version
        self.targetDigests['version'] = \
            'dd0fe2b83d102d906563e47e488014b20c85462f'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class Package(BinaryPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )

    def install(self):
        sourcedir = os.path.join( self.installDir(),
                        "gpg-w32-dev-"+self.buildTarget)
        for dir in glob.glob(sourcedir+"/*"):
            shutil.move( dir , self.installDir() )
        os.rmdir(sourcedir)
        return True

if __name__ == '__main__':
    Package().execute()
