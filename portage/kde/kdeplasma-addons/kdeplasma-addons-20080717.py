import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeplasma-addons'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdebase-runtime'] = 'default'
        self.dependencies['kde/kdebase-workspace'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()
