import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'
    
    def setDependencies( self ):
        if not os.getenv('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES'):
            self.hardDependencies['gnuwin32/wget'] = 'default'
            self.hardDependencies['gnuwin32/patch'] = 'default'

from Package.BinaryPackageBase import *
        
class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__(self)
    
if __name__ == '__main__':
    Package().execute()
