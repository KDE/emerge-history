# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# This is an example package for building a kdeedu application

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '4.6' ] = ""
        self.defaultTarget = '4.6'

    def setDependencies( self ):
        self.dependencies[ 'kde-4.6/parley' ] = 'default'

class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
#        whitelists = [ 'whitelist.txt' ]
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt', 'blacklist-mysql.txt', 'blacklist-virtuoso.txt' ]
        NullsoftInstallerPackager.__init__( self, blacklists=blacklists )
        VirtualPackageBase.__init__( self )
        self.defines[ "executable" ] = "bin\\parley.exe"

if __name__ == '__main__':
    Package().execute()
