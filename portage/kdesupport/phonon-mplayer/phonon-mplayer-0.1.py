# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.hardDependencies['testing/mplayer'] = 'default'

    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'git://git.kde.org/phonon-mplayer'
      self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = '-DPHONON_BUILDSYSTEM_DIR=\"%s\" ' % os.path.join(os.getenv('KDEROOT'),'share','phonon-buildsystem').replace('\\','/')


if __name__ == '__main__':
    Package().execute()
