import info
import compiler
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/runtime'
        self.svnTargets['komobranch'] = 'branches/work/komo/kdebase/runtime'
        if emergePlatform.isCrossCompilingEnabled():
            self.defaultTarget = 'komobranch'
        else:
            self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/oxygen-icons'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-bin/libssh'] = 'default'
        if compiler.isMinGW_WXX():
#            self.dependencies['win32libs-bin/libbfd'] = 'default'
            self.dependencies['win32libs-sources/libbfd-src'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += "-DDISABLE_ALL_OPTIONAL_SUBDIRECTORIES=TRUE "

        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")

        if self.isTargetBuild():
            self.subinfo.options.configure.defines += "-DKDEBASE_DISABLE_MULTIMEDIA=ON "
        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()
