import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-bin/exiv2'] = 'default'
        else:
            #FIXME make strigi svnHEAD compile on Windows
            # This hack is needed to get a different Version of
            # strigi for the Host platform
            self.buildDependencies['enterprise5/strigi-e5'] = 'default'
        self.dependencies['win32libs-bin/win_iconv'] = 'default'
        self.dependencies['win32libs-bin/libbzip2'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'
        if os.getenv('KDECOMPILER') == "msvc2010" and os.getenv('EMERGE_BUILDTYPE') == "Debug":
            # we cannot use Package methods here - we should have a pointer to
            # the package having instantiated us
            # the downloaded binary of clucene is compiled without Debug and msv2010 cannot
            # link it against strigi
            self.buildDependencies['win32libs-sources/clucene-core-src'] = 'default'
        else:
            self.buildDependencies['win32libs-bin/clucene-core'] = 'default'


    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://anongit.kde.org/strigi'
        self.svnTargets['komobranch'] = 'branches/work/komo/strigi'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/strigi'
        for i in ['4.4.0', '4.4.1', '4.4.2', '4.4.3', '4.4.4', '4.4']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.4/strigi'

        for ver in ['0.7.2']:
          self.targets[ver] ='http://www.vandenoever.info/software/strigi/strigi-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'strigi-' + ver
        self.patchToApply['0.7.2'] = ("strigi-0.7.2-20101223.diff", 1)
        self.targetDigests['0.7.2'] = 'b4c1472ef068536acf9c5c4c8f033a97f9c69f9f'

        self.shortDescription = "a desktop search engine and indexer"
        if emergePlatform.isCrossCompilingEnabled():
          #FIXME make strigi svnHEAD compile on Windows
          self.defaultTarget = 'komobranch'
        else:
          self.defaultTarget = '0.7.2'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.defines = ""
        if emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += "-DBUILD_DEEPTOOLS=OFF "
            self.subinfo.options.configure.defines += "-DBUILD_UTILS=OFF "
            self.subinfo.options.configure.defines += "-DENABLE_CPPUNIT=OFF "
            self.subinfo.options.configure.defines += "-DENABLE_XINE=OFF "
            self.subinfo.options.configure.defines += "-DENABLE_FFMPEG=OFF "
            self.subinfo.options.configure.defines += "-DENABLE_EXIV2=OFF "
            self.subinfo.options.configure.defines += "-DENABLE_INOTIFY=OFF "
            self.subinfo.options.configure.defines += "-DENABLE_POLLING=OFF "
            self.subinfo.options.configure.defines += "-DENABLE_FAM=OFF "
            self.subinfo.options.configure.defines += "-DENABLE_LOG4CXX=OFF "

        if self.buildTarget == "gitHEAD":
            self.subinfo.options.configure.defines = (
                " -DSTRIGI_SYNC_SUBMODULES=ON "
                " -DGIT_EXECUTABLE=%s "
                % os.path.join(self.rootdir, "dev-utils", "git", "bin",
                               "git.exe"))

        qmake = os.path.join(self.mergeDestinationDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            utils.warning("could not find qmake in <%s>" % qmake)
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += "-DQT_QMAKE_EXECUTABLE:FILEPATH=%s " \
            % qmake.replace('\\', '/')

if __name__ == '__main__':
    Package().execute()
