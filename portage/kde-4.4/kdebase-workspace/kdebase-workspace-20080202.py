# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.4/kdebase/workspace'
        for ver in ['90', '95']:
          self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.3.' + ver + '/src/kdebase-workspace-4.3.' + ver + '.tar.bz2'
          self.targetInstSrc['4.3.' + ver] = 'kdebase-workspace-4.3.' + ver
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.4.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.4.' + ver + '/src/kdebase-workspace-4.4.' + ver + '.tar.bz2'
          self.targetInstSrc['4.4.' + ver] = 'kdebase-workspace-4.4.' + ver
        self.patchToApply['4.3.90'] = ('kdebase-workspace-4.3.90.diff', 1)
        self.patchToApply['4.3.95'] = ('kdebase-workspace-4.3.95.diff', 1)
        self.patchToApply['4.4.0'] = ('kdebase-workspace-4.4.0.diff', 1)
        self.patchToApply['4.4.1'] = ('kdebase-workspace-4.4.1.diff', 1)
        self.patchToApply['4.4.4'] = ('kdebase-workspace-4.4.4.diff', 1)
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde-4.4/kdelibs'] = 'default'
        self.hardDependencies['kde-4.4/kdepimlibs'] = 'default'
        self.hardDependencies['kde-4.4/kdebase-runtime'] = 'default'
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
