import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepimlibs|komo3'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdepimlibs-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdepimlibs-4.0.' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/akonadi'] = 'default'
        self.dependencies['win32libs-bin/cyrus-sasl'] = 'default'
        self.dependencies['win32libs-bin/libical'] = 'default'
        self.dependencies['win32libs-bin/boost'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-bin/gpgme'] = 'default'
        else:
            self.dependencies['contributed/gpg4win-dev'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.boost = portage.getPackageInstance('win32libs-bin','boost')
        path = self.boost.installDir()
        os.putenv( "BOOST_ROOT", path )

        self.subinfo.options.configure.defines = "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")

        if emergePlatform.isCrossCompilingEnabled():
            if self.isTargetBuild():
                self.subinfo.options.configure.defines += "-DKDEPIM_NO_KRESOURCES=ON -DMAILTRANSPORT_INPROCESS_SMTP=ON "
        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()
