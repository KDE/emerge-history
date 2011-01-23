# -*- coding: utf-8 -*-
import info

from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.4.4'] = 'ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-1.4.4.tar.bz2'
        self.targetInstSrc['1.4.4'] = 'libgcrypt-1.4.4'
        self.patchToApply['1.4.4'] = ('libgcrypt-1.4.4-20091017.diff', 1)
        self.defaultTarget = '1.4.4'
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['win32libs-sources/gpg-error-src'] = 'default'
        self.hardDependencies['virtual/bin-base'] = 'default'
        self.hardDependencies['dev-util/msys'] = 'default'

class Package(PackageBase, MultiSource, AutoToolsBuildSystem, MultiPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        MultiPackager.__init__(self)
        self.buildInSource = True

if __name__ == '__main__':
    Package().execute()
