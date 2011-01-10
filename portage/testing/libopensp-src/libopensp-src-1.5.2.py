import info

SRC_URI= """
http://surfnet.dl.sourceforge.net/project/openjade/opensp/1.5.2/OpenSP-1.5.2.tar.gz
"""

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.5.2'] = SRC_URI
        self.targetInstSrc['1.5.2'] = "OpenSP-1.5.2"
        self.patchToApply['1.5.2'] = ( "OpenSP-1.5.2-20110111.diff", 1 )
        self.defaultTarget = '1.5.2'
        
from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )        

if __name__ == '__main__':
    Package().execute()

