import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.5'] = 'branches/KDE/4.5/kdemultimedia'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdemultimedia'
        for ver in ['60']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.1.' + ver + '/src/kdemultimedia-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdemultimedia-4.1.' + ver
        self.defaultTarget = '4.5'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.5/kdelibs'] = 'default'
        self.hardDependencies['kdesupport/taglib'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()