import info

class subinfo (info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['0.9.16a'] = "http://downloads.sourceforge.net/sourceforge/clucene/clucene-core-0.9.16a.tar.bz2"
        self.targetInstSrc['0.9.16a'] = os.path.join( "clucene-core-0.9.16a", "src" )
        self.targets['0.9.20'] = "http://downloads.sourceforge.net/sourceforge/clucene/clucene-core-0.9.20.tar.bz2"
        self.targetInstSrc['0.9.20'] = os.path.join( "clucene-core-0.9.20", "src" )
        self.targets['0.9.21b'] = "http://downloads.sourceforge.net/sourceforge/clucene/clucene-core-0.9.21b.tar.bz2"
        self.targetInstSrc['0.9.21b'] = os.path.join( "clucene-core-0.9.21b", "src" )
        self.defaultTarget = '0.9.21b'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DCLUCENE_VERSION:STRING="+self.buildTarget
        self.subinfo.options.configure.configurePath = "src"

    def unpack( self ):
        if not CMakePackageBase.unpack( self ):
            return True

        # we have an own cmake script - copy it to the right place
        cmake_script = ""
        if self.buildTarget == '0.9.16a':
            cmake_script = os.path.join( self.packageDir() , "CMakeLists-0.9.16.txt" )
        else:
            cmake_script = os.path.join( self.packageDir() , "CMakeLists-0.9.20.txt" )
        cmake_dest = os.path.join( self.sourceDir(), "CMakeLists.txt" )
        utils.copyFile( cmake_script, cmake_dest )
        cmake_script = os.path.join( self.packageDir() , "clucene-config.h.cmake" )
        cmake_dest = os.path.join( self.sourceDir(), "Clucene", "clucene-config.h.cmake" )
        utils.copyFile( cmake_script, cmake_dest )

        return True
    
if __name__ == '__main__':
    Package().execute()
