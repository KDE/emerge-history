# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision svn1207325

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '1.14', '1.15', '1.12', '1.13', '1.9', '1.19', '1.19-3', '1.19-1', '1.19-4', '1.19-5' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'libidn', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'libidn', version , '.tar.bz2.sha1' )

        self.defaultTarget = '1.19-5'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
