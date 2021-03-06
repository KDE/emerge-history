import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepim-runtime'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['kde/kde-runtime'] = 'default'
        else:
            self.dependencies['kdesupport/oxygen-icons'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['kdesupport/grantlee'] = 'default'
        self.dependencies['win32libs-bin/sqlite'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON "

        if emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += "-DDISABLE_ALL_OPTIONAL_SUBDIRECTORIES=TRUE "
            self.subinfo.options.configure.defines += " -DKDEPIM_MOBILE_UI=TRUE "
            self.subinfo.options.configure.defines += " -DBUILD_mobile=ON -DBUILD_messagecomposer=ON  -DBUILD_runtime=ON -DBUILD_strigi-analyzer=ON "
            self.subinfo.options.configure.defines += " -DMESSAGEVIEWER_NO_WEBKIT=ON "
            self.subinfo.options.configure.defines += " -DTEMPLATEPARSER_NO_WEBKIT=ON "
            #self.subinfo.options.configure.defines += " -DIMAPRESOURCE_NO_SOLID=ON "
            self.subinfo.options.configure.defines += " -DRUNTIME_PLUGINS_STATIC=ON "
            self.subinfo.options.configure.defines += " -DKDEQMLPLUGIN_STATIC=ON "
            self.subinfo.options.configure.defines += " -DACCOUNTWIZARD_NO_GHNS=ON "
            self.subinfo.options.configure.defines += " -DBUILD_kmail=ON "
            self.subinfo.options.configure.defines += " -DKDEPIM_NO_NEPOMUK=ON "
            self.subinfo.options.configure.defines += " -DKDE4_BUILD_TESTS=OFF "
            self.subinfo.options.configure.defines += " -DBUILD_kleopatra=ON "
            self.subinfo.options.configure.defines += " -DBUILD_korganizer=ON "
            self.subinfo.options.configure.defines += " -DKDEPIM_ENTERPRISE_BUILD=ON "
            self.subinfo.options.configure.defines += " -DKORGAC_AKONADI_AGENT=ON "
            self.subinfo.options.configure.defines += " -DBUILD_NEW_MAIL_NOTIFIER_AGENT=ON "
            self.subinfo.options.configure.defines += " -DAKONADI_USE_STRIGI_SEARCH=ON "
            self.subinfo.options.configure.defines += " -DKDEPIM_INPROCESS_LDAP=ON "
        else:
            self.subinfo.options.configure.defines += " -DKDEPIM_BUILD_MOBILE=FALSE "
        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF "

        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")

    def install( self ):
        if not CMakePackageBase.install( self ):
            return False
        if compiler.isMinGW():
            manifest = os.path.join( self.packageDir(), "akonadi_maildispatcher_agent.exe.manifest" )
            executable = os.path.join( self.installDir(), "bin", "akonadi_maildispatcher_agent.exe" )
            utils.embedManifest( executable, manifest )
        return True

if __name__ == '__main__':
    Package().execute()
