import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:attica||53963bd7340727c7df222583fd54c6b704371e77'

        for ver in ['0.1.3','0.2.0']:
          self.targets[ver] ='http://download.kde.org/download.php?url=stable/attica/attica-' + ver +'.tar.bz2'
          self.targetInstSrc[ver] = 'attica-' + ver
        self.shortDescription = "implements the Open Collaboration Services API"
        self.defaultTarget = 'gitHEAD'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

        self.subinfo.options.configure.defines = ""
        qmake = os.path.join(self.mergeDestinationDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            utils.warning("could not find qmake in <%s>" % qmake)
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += "-DQT_QMAKE_EXECUTABLE:FILEPATH=%s " \
            % qmake.replace('\\', '/')

if __name__ == '__main__':
    Package().execute()
