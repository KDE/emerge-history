import info

static = False

class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'
        if static: 
            self.buildDependencies[ 'libs/qt-static' ] = 'default'
        else:
            self.dependencies[ 'libs/qt' ] = 'default'
        self.buildDependencies[ 'dev-util/upx' ] = 'default'

    def setTargets( self ):
        self.svnTargets[ 'svnHEAD' ] = '[git]kde:automoc'
        self.defaultTarget = 'svnHEAD'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        if static: 
            self.qtstatic = portage.getPackageInstance( 'libs', 'qt-static' )
            qmake = os.path.join( self.qtstatic.installDir(), "bin", "qmake.exe" )
            if not os.path.exists( qmake ):
                utils.warning( "could not find qmake in <%s>" % qmake )
            ## \todo a standardized way to check if a package is installed in the image dir would be good.
            self.subinfo.options.configure.defines = "-DAUTOMOC_STATIC -DQT_QMAKE_EXECUTABLE:FILEPATH=%s" \
                % qmake.replace( '\\', '/' )

if __name__ == '__main__':
    Package().execute()
