# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision svn1224614

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '0.1.0', '0.1.1', '0.2.1', '0.2.1-1' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'ebook-tools', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'ebook-tools', version, '.tar.bz2.sha1' )

        self.defaultTarget = '0.2.1-1'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/libzip' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/libxml2' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
