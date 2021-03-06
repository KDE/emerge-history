import base
import utils
from utils import die
import sys
import info

# see http://eigen.tuxfamily.org/ for more informations

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        for ver in ['2.0.10','2.0.15', '2.0.16']:
            self.targets[ver] = 'http://bitbucket.org/eigen/eigen/get/' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'eigen'
        self.targetInstSrc['2.0.16'] = 'eigen-eigen-9ca09dbd70ce'
        self.targetDigests['2.0.16'] = 'ec0d6e6716b7e3ce916ca0ff378a346d710c8db2'
        self.defaultTarget = '2.0.16'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_TESTS=OFF"
        # header-only package
        self.subinfo.options.package.withCompiler = False

if __name__ == '__main__':
    Package().execute()
