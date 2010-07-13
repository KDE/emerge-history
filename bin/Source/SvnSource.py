# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# subversion support
## \todo needs dev-utils/subversion package, add some kind of tool requirement tracking for SourceBase derived classes 

from VersionSystemSourceBase import *

import os.path
import utils

import traceback
import tempfile
import getpass

if os.name == 'nt': import msvcrt
else:               import fcntl

SVN_LOCK_FILE = "emergesvn-%s.lck"

def svn_lock_file_name():
    '''Generate a user global svn lock file.
       TODO: generate it smarter to prevent security issues
             and possible collisions.
    '''
    return os.path.join(
        tempfile.gettempdir(), SVN_LOCK_FILE % getpass.getuser())

class Locker(object):
    """Context manager for a user global SVN lock"""

    def __init__(self, file_name):
        self.file_name   = file_name
        self.file_handle = None

    def __enter__(self):
        do_lock = os.environ.get("EMERGE_SVN_LOCK")
        if not do_lock or do_lock.strip().lower() not in ("true", "yes"):
            return

        self.file_handle = open(self.file_name, 'a')
        fh = self.file_handle

        if os.name == 'nt':
            fh.seek(0)
            while True:
                try:
                    msvcrt.locking(fh.fileno(), msvcrt.LK_LOCK, 2147483647L)
                except IOError, msg:
                    # after 15 secs (every 1 sec, 1 attempt -> 15 secs)
                    # a exception is raised but we want to continue trying.
                    continue
                break
        else:
            fcntl.flock(fh, fcntl.LOCK_EX)

        fh.truncate(0)
        print >> fh, "%d" % os.getpid()
        fh.flush()

    def __exit__(self, exc_type, exc_value, exc_tb):
        fh = self.file_handle
        if fh is None: return
        self.file_handle = None
        if os.name == 'nt':
            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 2147483647L)
        else:
            fcntl.flock(fh, fcntl.LOCK_UN)
        try:
            fh.close()
        except:
            traceback.print_exc()

class SvnSource (VersionSystemSourceBase):
    """subversion support"""
    def __init__(self):
        VersionSystemSourceBase.__init__(self)
        self.options = None
        ## \todo add internal dependency for subversion package
        self.svnInstallDir = os.path.join(self.rootdir,'dev-utils','svn','bin')
        if not os.path.exists(self.svnInstallDir):
            utils.die("required subversion package not installed in %s" % self.svnInstallDir)
            
    def setProxy(self):
        """set proxy for fetching sources from subversion repository"""
        (host, port, username, password) = self.proxySettings()
        if host == None:
            return 

        proxyOptions = " --config-option servers:global:http-proxy-host=%s" % host
        proxyOptions += " --config-option servers:global:http-proxy-port=%s" % port
        if username != None:
            proxyOptions += " --config-option servers:global:http-proxy-username=%s" % username
            proxyOptions += " --config-option servers:global:http-proxy-password=%s" % password
        
        self.options = proxyOptions
            
    def fetch( self ):
        """ checkout or update an existing repository path """
        if self.noFetch:
            utils.debug( "skipping svn fetch (--offline)" )
            return True

        for i in range(0, self.repositoryUrlCount()):
            url = self.repositoryUrl(i)
            sourcedir = self.sourceDir(i)
            if self.repositoryUrlOptions(i) == 'norecursive':
                self.__tryCheckoutFromRoot(url,sourcedir,False)
            else:
                self.__tryCheckoutFromRoot(url,sourcedir,True)
            i += 1
        return True

    def __splitPath(self, path):
        """ split a path into a base part and a relative repository url. 
        The delimiters are currently 'trunk', 'branches' and 'tags'. 
        """
        pos=path.find('trunk')
        if pos == -1:
            pos=path.find('branches')
            if pos == -1:
                pos=path.find('tags')
        if pos == -1:
            ret = [path,None]
        else:
            ret = [path[:pos-1], path[pos:]]
        return ret

    def __tryCheckoutFromRoot ( self, url, sourcedir, recursive=True ):
        """This method checkout source with svn informations from 
        the svn root repository directory. It detects the svn root 
        by searching the predefined root subdirectories 'trunk', 'branches' 
        and 'tags' which will probably fit for most servers
        """
        (urlBase,urlPath) = self.__splitPath(url)
        if urlPath == None:
            return self.__checkout(url, sourcedir, recursive)
        
        (srcBase,srcPath)  = self.__splitPath(sourcedir)
        if srcPath == None: 
            return self.__checkout(url, sourcedir, recursive)
        
        urlRepo = urlBase
        srcDir = srcBase
        urlParts = urlPath.split('/')
        pathSep = '/'
        srcParts = srcPath.split(pathSep)
        
        # url and source parts not match 
        if len(urlParts) <> len(srcParts):
            return self.__checkout(url, sourcedir, recursive)
        
        for i in range(0,len(urlParts)-1):
            urlPart = urlParts[i]
            srcPart = srcParts[i]
            if ( urlPart == "" ):
                continue
            
            urlRepo +=  '/' + urlPart
            srcDir +=  pathSep + srcPart
            
            if os.path.exists(srcDir): 
                continue
            self.__checkout( urlRepo, srcDir, False )
            
        self.__checkout( url, sourcedir, recursive )
    
    def __checkout( self, url, sourcedir, recursive=True ):
        """internal method for subversion checkout and update"""
        option = ""
        if not recursive:
            option = "--depth=files" 
            
        if utils.verbose() < 2: 
            option += " --quiet"
          
        self.setProxy()
        
        if self.options != None:
            option += self.options
            
        if self.subinfo.options.fetch.ignoreExternals:
            option += " --ignore-externals "

        url = utils.replaceVCSUrl( url )

        if os.path.exists( sourcedir ):
            cmd = "%s/svn update %s %s %s" % ( self.svnInstallDir, option, url, sourcedir )
        else:
            cmd = "%s/svn checkout %s %s %s" % (self.svnInstallDir, option, url, sourcedir )

        with Locker(svn_lock_file_name()):
            return utils.system( cmd )

    def createPatch( self ):
        """create patch file from svn source into the related package dir. The patch file is named autocreated.patch"""
        cmd = "%s/svn diff %s > %s" % ( self.svnInstallDir, self.sourceDir(), os.path.join( self.packageDir(), "%s-%s.patch" % ( self.package, str( datetime.date.today() ).replace('-', '') ) ) )
        with Locker(svn_lock_file_name()):
            return utils.system( cmd )

    def sourceVersion( self ):
        """ return the revision returned by svn info """
        # first, change the output to always be english
        if "LANG" in os.environ:
            oldLanguage = os.environ["LANG"]
        else:
            oldLanguage = ""
        os.environ["LANG"] = "C"
        
        # set up the command
        cmd = "%s/svn info %s" % ( self.svnInstallDir, self.sourceDir() )

        # open a temporary file - do not use generic tmpfile because this doesn't give a good file object with python
        tempfile = open( os.path.join( self.sourceDir().replace('/', '\\'), ".emergesvninfo.tmp" ), "wb+" )
        
        # run the command
        with Locker(svn_lock_file_name()):
            utils.system( cmd, outstream=tempfile )

        tempfile.seek(os.SEEK_SET)
        # read the temporary file and find the line with the revision
        for line in tempfile:
            if line.startswith("Revision: "):
                revision = line.replace("Revision: ", "").strip()
                break
        tempfile.close()
        
        # print the revision - everything else should be quiet now
        print revision
        os.environ["LANG"] = oldLanguage
        os.remove( os.path.join( self.sourceDir().replace('/', '\\'), ".emergesvninfo.tmp" ) )
        return True
