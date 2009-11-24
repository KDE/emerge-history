import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdepimlibs'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdepimlibs'
        self.defaultTarget = '20091123'
    
    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdelibs'] = 'default'
        self.hardDependencies['win32libs-bin/libical'] = 'default'
        self.hardDependencies['win32libs-bin/gpgme'] = 'default'
        self.hardDependencies['win32libs-bin/cyrus-sasl'] = 'default'
        self.hardDependencies['enterprise5/akonadi-e5'] = 'default'
        self.hardDependencies['win32libs-bin/boost'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.boost = portage.getPackageInstance('win32libs-bin','boost')
        path = self.boost.installDir()
        os.putenv( "BOOST_ROOT", path )

if __name__ == '__main__':
    Package().execute()
