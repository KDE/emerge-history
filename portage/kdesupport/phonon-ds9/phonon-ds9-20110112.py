import info
import compiler
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.dependencies['kdesupport/phonon'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://git.kde.org/phonon-directshow'
        self.shortDescription = "the DirectShow based phonon multimedia backend"
        self.defaultTarget = 'gitHEAD'

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
