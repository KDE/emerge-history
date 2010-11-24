import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdepimlibs'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdepimlibs'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdepimlibs-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdepimlibs-4.0.' + ver
        self.defaultTarget = 'svnHEAD'

        if emergePlatform.isCrossCompilingEnabled():
            #TODO: Fix it so that it works on Windows NT and upstream it into
            # kdepimlibs.
            self.patchToApply['svnHEAD'] = ('winldap-patch.diff', 1)
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kdesupport/akonadi'] = 'default'
        self.hardDependencies['win32libs-sources/cyrus-sasl-src'] = 'default'
        self.hardDependencies['win32libs-sources/libical-src'] = 'default'
        self.hardDependencies['win32libs-bin/boost'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-bin/gpgme'] = 'default'
        else:
            self.hardDependencies['contributed/gpg4win-dev'] = 'default'

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
            self.subinfo.options.configure.defines += "-DBUILD_doc=OFF "
            if self.isTargetBuild():
                self.subinfo.options.configure.defines += "-DKDEPIM_NO_KRESOURCES=ON -DMAILTRANSPORT_INPROCESS_SMTP=ON "

if __name__ == '__main__':
    Package().execute()
