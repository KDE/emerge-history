import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdetoys'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()
