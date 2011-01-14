import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/extragear/utils/krusader"
        self.targets['2.0.0-beta2'] = 'http://prdownloads.sourceforge.net/krusader/krusader-2.0.0-beta2.tar.gz'
        self.targetInstSrc['2.0.0-beta2'] = 'krusader-2.0.0-beta2'
        self.patchToApply['2.0.0-beta2'] = ['krusader.patch',1]
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/kdebase-runtime'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
