import info
import os

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'svnHEAD' ] = 'svn://svn.gna.org/svn/kbibtex/trunk'
        # no "release" targets defined, yet.
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies[ 'virtual/kde-runtime' ] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

