# -*- coding: utf-8 -*-
import info
import tempfile
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.3'] = "http://winkde.org/pub/kde/ports/win32/repository/other/Git-1.6.3-preview20090507-2.tar.bz2"
        self.targetInstSrc['1.6.3'] = ""
        self.targets['1.6.4'] = "http://msysgit.googlecode.com/files/PortableGit-1.6.4-preview20090729.7z"
        self.targets['1.7.0.2'] = "http://msysgit.googlecode.com/files/PortableGit-1.7.0.2-preview20100309.7z"
        self.targetDigests['1.7.0.2'] = '96c3720dec940c4b8da8a09bfdcfa7ed56c2f016'

        self.defaultTarget = '1.7.0.2'

    def setDependencies(self):
        self.buildDependencies['dev-util/7zip']   = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils/git";
        BinaryPackageBase.__init__(self)

    def unpack(self):
        if not BinaryPackageBase.unpack(self):
            return False
        utils.copyFile(os.path.join(self.packageDir(),"git.bat"),os.path.join(self.rootdir,"dev-utils","bin","git.bat"))
        utils.copyFile(os.path.join(self.packageDir(),"gb.bat"),os.path.join(self.rootdir,"dev-utils","bin","gb.bat"))
        utils.copyFile(os.path.join(self.packageDir(),"gitk.bat"),os.path.join(self.rootdir,"dev-utils","bin","gitk.bat"))
        return True

    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
            return False
        tmpFile = tempfile.TemporaryFile()
        git = os.path.join(self.rootdir,"dev-utils","git","bin","git")
        utils.system( "%s config --global --get url.git://anongit.kde.org/.insteadof" % git,
            stdout=tmpFile, stderr=tmpFile  )
        tmpFile.seek( 0 )
        for line in tmpFile:
            if line.find("kde:")>-1:
                return True
        utils.debug( "adding kde related settings to global git config file",1 )
        utils.system( "%s config --global url.git://anongit.kde.org/.insteadOf kde:" % git)
        utils.system( "%s config --global url.ssh://git@git.kde.org/.pushInsteadOf kde:" % git)
        utils.system( "%s config --global core.autocrlf false")
        return True

if __name__ == '__main__':
    Package().execute()
