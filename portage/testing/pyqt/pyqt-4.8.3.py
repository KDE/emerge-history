import base
import utils
import sys
import info
import os
import compiler
import sipconfig
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.buildDependencies['testing/sip'] = 'default'

    def setTargets( self ):
        self.targets['4.8.3'] = 'http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-win-gpl-4.8.3.zip'
        self.targetInstSrc['4.8.3'] = 'PyQt-win-gpl-4.8.3'
        self.targetDigests['4.8.3'] = '737e6ff98a4c0e5149035733928203b12d09a247'
        self.defaultTarget = '4.8.3'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        # jom reports missing moc_translator.xxx
        self.subinfo.options.make.supportsMultijob = False
        # add support for other location based on pythonpath
        localPythonPath = os.path.join(self.rootdir, 'emerge', 'python')
        haveLocalPython = os.path.exists(localPythonPath)
        if haveLocalPython:
            self.subinfo.options.merge.destinationPath = "emerge/python"
        self.subinfo.options.configure.defines = " --confirm-license --verbose"
        if self.buildType() == "Debug":
            self.subinfo.options.configure.defines += " -u"

        if compiler.isMSVC2008():
            specName = "win32-msvc2008"
        elif compiler.isMSVC2010():
            specName = "win32-msvc2010"
        elif compiler.isMinGW():
            specName = "win32-g++"
        else:
            utils.die("compiler %s not supported for PyQt4" % compiler.COMPILER)
        if haveLocalPython:
           specDir = self.mergeDestinationDir()
        else:
           specDir = self.rootdir
        os.putenv("QMAKESPEC", os.path.join(specDir, "mkspecs", specName))

    def configure( self ):
        self.enterSourceDir()
        
        cmd = "python configure.py"
        cmd += self.subinfo.options.configure.defines
        cmd += " --bindir %s/bin " % self.installDir() 
        cmd += " --destdir %s/Lib/site-packages " % self.installDir() 
        cmd += " --plugin-destdir %s/plugins " % self.installDir() 

        sipcfg = sipconfig.Configuration()
        sipdir = os.path.splitdrive(sipcfg.default_sip_dir)[1]
        sipdir = os.path.join(sipdir,'PyQt4')
        cmd += " --sipdir %s%s " % (self.installDir(), sipdir)
        
        utils.system(cmd) or utils.die("command: %s failed" % (cmd))

        return True

    def make( self ):
        self.enterSourceDir()
        utils.system(self.makeProgramm) or utils.die("command: %s failed" % self.makeProgramm)
        return True

    def install( self ):
        self.enterSourceDir()
        cmd = self.makeProgramm + " install"
        utils.system(cmd) or utils.die("command: %s failed" % cmd)
        return True

    def runTest(self):
        return False

if __name__ == '__main__':
    Package().execute()
