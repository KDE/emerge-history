import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
		# will be moved to kdewin-qt 
        self.hardDependencies['libs/qt'] = 'default'
		# will be moved to kdewin-tools
        self.hardDependencies['win32libs-bin/zlib'] = 'default'
        self.hardDependencies['win32libs-bin/libpng'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.3.9'] = 'tags/kdewin32/0.3.9'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/kdewin'
        self.patchToApply['svnHEAD'] = ("kdewin-20100527.patch", 1)
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.package.version = '0.5.2'
        self.subinfo.options.configure.defines = '-DBUILD_BASE_LIB_WITH_QT=On -DBUILD_QT_LIB=On -DBUILD_TOOLS=On'
        CMakePackageBase.__init__( self )
        
        self.subinfo.options.configure.defines = ""
        qmake = os.path.join(self.mergeDestinationDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            print("<%s>") % qmake
            utils.die("could not found qmake")
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += "-DQT_QMAKE_EXECUTABLE:FILEPATH=%s " \
            % qmake.replace('\\', '/')

if __name__ == '__main__':
    Package().execute()
