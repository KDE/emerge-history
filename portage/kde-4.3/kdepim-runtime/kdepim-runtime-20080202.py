import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.3.' + ver + '/src/kdepim-runtime-4.3.' + ver + '.tar.bz2'
          self.targetInstSrc['4.3.' + ver] = 'kdepim-runtime-4.3.' + ver
        self.patchToApply['4.3.4'] = ( 'kdepim-runtime-4.3.4.diff', 1 )
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde-4.3/kdebase-runtime'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
