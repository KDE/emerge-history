import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/office/skrooge'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['virtual/kdebase-runtime']    = 'default'
        self.dependencies['win32libs-bin/libopensp'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
