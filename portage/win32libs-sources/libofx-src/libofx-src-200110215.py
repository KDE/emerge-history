import info
import compiler

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['0.9.1'] = "http://downloads.sourceforge.net/project/libofx/libofx/0.9.1/libofx-0.9.1.tar.gz"
        self.targetInstSrc['0.9.1'] = "libofx-0.9.1"
        self.patchToApply['0.9.1'] = []
        if compiler.isMSVC():
            self.patchToApply['0.9.1'].append(("ofx-msvc.diff", 1))
        self.patchToApply['0.9.1'].append(("libofx-0.9.1-20110107.diff", 1))

        self.targets['0.9.2'] = "http://downloads.sourceforge.net/project/libofx/libofx/0.9.2/libofx-0.9.2.tar.gz"
        self.targetInstSrc['0.9.2'] = "libofx-0.9.2"
        self.patchToApply['0.9.2'] = []
        if compiler.isMSVC():
            self.patchToApply['0.9.2'].append(("ofx-msvc.diff", 1))
        self.patchToApply['0.9.2'].append(("libofx-0.9.2-20110215.diff", 1))

        self.shortDescription = "a parser and an API for the OFX (Open Financial eXchange) specification"
        self.defaultTarget = '0.9.2'

    def setDependencies( self ):
        self.dependencies['win32libs-bin/libopensp'] = 'default'
        self.dependencies['win32libs-bin/win_iconv'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        # we use subinfo for now too
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()

