import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.5'] = 'branches/KDE/4.5/kdeplasma-addons'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeplasma-addons'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdeplasma-addons-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdeplasma-addons-4.0.' + ver
        self.defaultTarget = '4.5'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.hardDependencies['kde-4.5/kdebase-workspace'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()