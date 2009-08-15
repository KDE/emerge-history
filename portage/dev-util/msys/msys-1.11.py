import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/mingw/msysCORE-1.0.11-20080826.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/gettext-devel-0.16.1-MSYS-1.0.11-1.tar.bz2
http://downloads.sourceforge.net/sourceforge/mingw/gettext-0.16.1-MSYS-1.0.11-1.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.11'] = SRC_URI
        self.defaultTarget = '1.11'
        # This attribute is in prelimary state
        ## \todo move to dev-utils/msys
        self.targetMergePath['1.11'] = "msys";
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
