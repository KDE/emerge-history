import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['4.6']:
            self.svnTargets[ ver ] = '[git]kde:kolourpaint|%s|' % ver
            
        self.svnTargets['gitHEAD'] = '[git]kde:kolourpaint'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/qimageblitz'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
