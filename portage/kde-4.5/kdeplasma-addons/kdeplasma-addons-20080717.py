import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.5/kdeplasma-addons'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.5.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.5.' + ver + '/src/kdeplasma-addons-4.5.' + ver + '.tar.bz2'
            self.targetInstSrc['4.5.' + ver] = 'kdeplasma-addons-4.5.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.dependencies['kde-4.5/kdebase-workspace'] = 'default'
        self.shortDescription = "several plasma specific addons"

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
