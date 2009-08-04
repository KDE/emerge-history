
from EmergeBase import *;
import os;
import utils;

class PackageBase (EmergeBase):
    """
     provides a generic interface for packages and implements the basic stuff for all
     packages
    """

    # uses the following instance variables 
    # todo: place in related ...Base
    
    #rootdir    -> EmergeBase  
    #package    -> PackageBase
    #force      -> PackageBase
    #category   -> PackageBase
    #version    -> PackageBase
    #packagedir -> PackageBase
    #imagedir   -> PackageBase
    
    def __init__(self):
        utils.debug("PackageBase.__init__ called",2)
        EmergeBase.__init__(self)
        self.forceCreateManifestFiles = False

    def __installedDBPrefix(self):
        if self.useBuildTypeRelatedMergeRoot:
            if self.buildType() == 'Debug':
                postfix = 'debug'
            elif self.buildType() == 'Release':
                postfix =  'release'
        else:
            postfix =  ''
        return postfix

    def qmerge( self ):
        """mergeing the imagedirectory into the filesystem"""
 
        ## \todo is this the optimal place for creating the post install scripts ? 
        # create post install scripts 
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packageDir(), "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            # are there any cases there installDir should be honored ? 
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                utils.createDir( os.path.join( self.imageDir(), "manifest" ) )
            if os.path.exists( script ):
                utils.copyFile( script, destscript )

        if portage.isInstalled( '', self.package, '', self.buildType() ):
            self.unmerge()

        utils.mergeImageDirToRootDir( self.mergeSourceDir(), self.mergeDestinationDir() )
        self.manifest()

        # run post-install scripts
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            script = os.path.join( self.rootdir, "manifest", scriptName )
            if os.path.exists( script ):
                cmd = "cd %s && %s" % ( self.rootdir, script )
                utils.system( cmd ) or utils.warning("%s failed!" % cmd )

        # add package to installed database -> is this not the task of the manifest files ? 
       
        portage.addInstalled( self.category, self.package, self.version, self.__installedDBPrefix() )
        return True

    def unmerge( self ):
        """unmergeing the files from the filesystem"""
        utils.debug("Packagebase unmerge called",2)

        ## \todo mergeDestinationDir() reads the real used merge dir from the 
        ## package definition, which fails if this is changed 
        ## a better solution will be to save the merge sub dir into 
        ## /etc/portage/installed and to read from it on unmerge
        utils.unmerge( self.mergeDestinationDir(), self.package, self.forced )
        portage.remInstalled( self.category, self.package, self.version, self.__installedDBPrefix() )
        return True

    def cleanup( self ):
        """cleanup before install to imagedir"""
        if hasattr(self,'buildSystemType') and self.buildSystemType == 'binary' or hasattr(self,'buildsystem') and self.buildsystem.buildSystemType == 'binary':
            utils.debug("skipped cleaning image dir because we use binary build system",1)
            return True
        if ( os.path.exists( self.imageDir() ) ):
            utils.debug( "cleaning image dir: %s" % self.imageDir(), 1 )
            utils.cleanDirectory( self.imageDir() )
        return True
        
    def manifest( self ):
        """installer compatibility: make the manifest files that make up the installers"""
        """install database"""
    
        utils.debug("base manifest called",2)
        if not utils.hasManifestFile( self.mergeDestinationDir(), self.category, self.package ) or self.forceCreateManifestFiles:
            utils.debug("creating of manifest files triggered", 1)
            utils.createManifestFiles( self.mergeSourceDir(), self.mergeDestinationDir(), self.category, self.package, self.version )
        return True

    def stripLibs( self, pkgName ):
        """strip debugging informations from shared libraries"""
        basepath = os.path.join( self.installDir() )
        dllpath = os.path.join( basepath, "bin", "%s.dll" % pkgName )

        cmd = "strip -s " + dllpath
        os.system( cmd )
        return True

    def createImportLibs( self, pkgName ):
        """create the import libraries for the other compiler(if ANSI-C libs)"""
        basepath = os.path.join( self.installDir() )
        utils.createImportLibs( pkgName, basepath )

    def execute( self, cmd=None ):
        """called to run the derived class"""
        """this will be executed from the package if the package is started on its own"""
        """it shouldn't be called if the package is imported as a python module"""

        utils.debug( "EmergeBase.execute called. args: %s" % sys.argv, 2 )

        self.setBuildTarget()

        if not cmd:
            command = sys.argv[ 1 ]
            options = ""
            if ( len( sys.argv )  > 2 ):
                options = sys.argv[ 2: ]
        else:
            command = cmd
            options = ""

        # \todo cleanup
        self.setDirectoriesBase()
        
        # \todo cleanup
        self.setDirectories()
        
        #if self.createCombinedPackage:
        #    oldBuildType = os.environ["EMERGE_BUILDTYPE"]                        
        #    os.environ["EMERGE_BUILDTYPE"] = "Release"
        #    self.runAction(command)
        #    os.environ["EMERGE_BUILDTYPE"] = "Debug"
        #    self.runAction(command)
        #    os.environ["EMERGE_BUILDTYPE"] = oldBuildType
        #else:
        self.runAction(command)

    def runAction( self, command ):
        ok = True
        utils.debug( "command: %s" % command,0 )
        if command   == "fetch":       ok = self.fetch()
        elif command == "cleanimage":  ok = self.cleanup()
        elif command == "unpack":      ok = self.unpack()
        elif command == "compile":     ok = self.compile()
        elif command == "configure":   ok = self.configure()
        elif command == "make":        ok = self.make()
        elif command == "install":     ok = self.install()
        elif command == "test":        ok = self.unittest()
        elif command == "qmerge":      ok = self.qmerge()
        elif command == "unmerge":     ok = self.unmerge()
        elif command == "manifest":    ok = self.manifest()
        elif command == "package":     ok = self.createPackage()
        else:
            ok = utils.error( "command %s not understood" % command )

        if ( not ok ):
            utils.die( "command %s failed" % command )
        