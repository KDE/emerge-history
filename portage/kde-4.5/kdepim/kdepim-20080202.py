# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdepim'
        self.svnTargets['4.5'] = 'branches/KDE/4.5/kdepim'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdepim'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdepim-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdepim-4.0.' + ver
        self.defaultTarget = '4.5'

    def setDependencies( self ):
        self.hardDependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.hardDependencies['kde-4.5/kdepimlibs'] = 'default'
        self.hardDependencies['kdesupport/grantlee'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON"
        #        self.subinfo.options.configure.defines += " -DBUILD_doc=OFF"

if __name__ == '__main__':
    Package().execute()