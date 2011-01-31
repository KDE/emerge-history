import info
import compiler
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.dependencies['kdesupport/phonon'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:phonon-directshow'
        self.shortDescription = "the DirectShow based phonon multimedia backend"
        self.defaultTarget = 'gitHEAD'

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = '-DPHONON_BUILDSYSTEM_DIR=\"%s\" ' % os.path.join(os.getenv('KDEROOT'),'share','phonon-buildsystem').replace('\\','/')

if __name__ == '__main__':
    Package().execute()
