import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/multimedia/kmid'
        for ver in ['2.3.0', '2.3.1', '2.4.0']:
          self.targets[ver] = 'http://downloads.sourceforge.net/kmid2/kmid-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'kmid-' + ver
        self.shortDescription = "a MIDI/Karaoke player for KDE4"
        self.defaultTarget = '2.4.0'

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
