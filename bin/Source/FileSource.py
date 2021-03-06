#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Source.SourceBase import *

class FileSource(SourceBase):
    """ file download source"""
    filenames = []
    def __init__(self, subinfo=None):
        utils.debug( "FileSource.__init__ called", 2 )
        if subinfo:
            self.subinfo = subinfo
        SourceBase.__init__( self )

    def localFileNamesBase(self):
        """ collect local filenames """
        utils.debug( "FileSource.localFileNamesBase called", 2 )

        filenames = []

        if self.subinfo.hasTarget():
            for uriPos in range( self.subinfo.targetCount() ):
                filenames.append( os.path.basename( self.subinfo.targetAt( uriPos ) ) )
        return filenames

    def localFileNames(self):
        # pylint: disable=E0202
        # but I have no idea why pylint thinks this overrides
        # MultiSource.localFileNames
        return self.localFileNamesBase()

    def fetch( self, dummyRepopath = None ):
        """fetching binary files"""
        utils.debug( "FileSource.fetch called", 2 )

        if ( self.noFetch ):
            utils.debug( "skipping fetch (--offline)" )
            return True

        self.setProxy()
        if self.subinfo.hasTarget():
            return utils.getFiles( self.subinfo.target(), self.downloadDir() )
        else:
            return utils.getFiles( "", self.downloadDir() )

    def unpack(self):
        """copying files into local dir"""
        utils.debug( "FileSource.unpack called", 2 )

        filenames = self.localFileNames()
        # if using BinaryBuildSystem the files should be unpacked into imagedir
        if self.buildSystemType == 'binary':
            destdir = self.installDir()
            if not os.path.exists(destdir):
                os.makedirs(destdir)
            utils.debug("unpacking files into image root %s" % destdir, 1)
        else:
            destdir = self.workDir()
            self.enterBuildDir()
            utils.debug("unpacking files into work root %s" % destdir, 1)

        for filename in filenames:
            filePath = os.path.abspath( os.path.join(self.downloadDir(), filename) )
            if self.subinfo.options.unpack.runInstaller: 
                _, ext = os.path.splitext( filename )
                if ext == ".exe":
                    return utils.system("%s" % filePath )
                elif ( ext == ".msi" ):
                    return utils.system("msiexec /package %s" % filePath )
            if not utils.copyFile( filePath, os.path.join(destdir, filename) ):
                return False
        return True
