# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

""" \package BuildSystemBase"""

from EmergeBase import *
import utils
import compiler


class BuildSystemBase(EmergeBase):
    """provides a generic interface for build systems and implements all stuff for all build systems"""
    noClean = False
    debug = True

    def __init__(self, type, className=None):
        """constructor"""
        EmergeBase.__init__(self, className)
        self.buildSystemType = type
        self.envPath = ""
        if self.compiler() == "mingw":
            self.envPath = "mingw/bin"
        if self.compiler() == "mingw4":
            self.envPath = "mingw4/bin"


    def _getmakeProgram(self):
        EMERGE_MAKE_PROGRAM = os.getenv( "EMERGE_MAKE_PROGRAM" )
        if EMERGE_MAKE_PROGRAM and self.subinfo.options.make.supportsMultijob:
            utils.debug( "set custom make program: %s" % EMERGE_MAKE_PROGRAM, 1 )
            return EMERGE_MAKE_PROGRAM
        elif not self.subinfo.options.make.supportsMultijob:
            os.unsetenv("MAKE")
        if compiler.isMSVC():
            return "nmake /NOLOGO"
        elif compiler.isMinGW_WXX():
            return "gmake"
        elif compiler.isMinGW32():
            return "mingw32-make"
        else:
            utils.die( "unknown %s compiler" % self.compiler() )
    makeProgramm = property(_getmakeProgram)
    
    def configure(self): 
        """configure the target"""
        abstract()

    def install(self): 
        """install the target into local install directory"""
        abstract()

    def uninstall(self): 
        """uninstall the target from the local install directory"""
        abstract()

    def runTests(self): 
        """run the test - if available - for the target"""
        abstract()

    def make(self): 
        """make the target by runnning the related make tool"""
        abstract()
            
    def compile(self):
        """convencience method - runs configure() and make()"""
        return self.configure() and self.make()
    
    def configureSourceDir(self):
        """returns source dir used for configure step"""
        if hasattr(self,'source'):
            sourcedir = self.source.sourceDir()
        else:
            sourcedir = self.sourceDir()
       
        if self.subinfo.hasConfigurePath():
            sourcedir = os.path.join(sourcedir, self.subinfo.configurePath())
        return sourcedir
        
    def configureOptions(self, defines=""):
        """return options for configure command line""" 
        if self.subinfo.options.configure.defines != None:
            defines += " %s" % self.subinfo.options.configure.defines
        return defines

    def makeOptions(self, defines=""):
        """return options for configure command line""" 
        if self.subinfo.options.make.ignoreErrors:
            command += " -i"
        if self.subinfo.options.make.makeOptions != None:
            defines += " %s" % self.subinfo.options.make.makeOptions
        return defines
        
    def setupTargetToolchain(self):
        os.environ["PATH"] = os.environ["TARGET_PATH"]
        os.environ["INCLUDE"] = os.environ["TARGET_INCLUDE"]
        os.environ["LIB"] = os.environ["TARGET_LIB"]

    def dumpDependencies(self):
        """dump package dependencies """
        abstract()
