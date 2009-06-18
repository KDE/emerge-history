import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.1'] = 'branches/kdepim/enterprise4/kdelibs-4.1-branch'
        self.svnTargets['4.2'] = 'branches/kdepim/enterprise4/kdelibs-4.2-branch'
        for ver in ['74', '80', '83']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdelibs-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdelibs-enterprise4-4.0.' + ver
        self.defaultTarget = '4.1'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl']       = 'default'

        self.hardDependencies['enterprise4/qt'] = 'default'

        self.hardDependencies['win32libs-sources/aspell-src']  = 'default'
#        self.hardDependencies['win32libs-sources/enchant-src']  = 'default'
        self.hardDependencies['win32libs-sources/gettext-src']  = 'default'
        self.hardDependencies['win32libs-sources/giflib-src']  = 'default'
#        self.hardDependencies['win32libs-sources/gssapi-src']  = 'default'
#        self.hardDependencies['win32libs-sources/hspell-src']  = 'default'
        self.hardDependencies['win32libs-sources/jasper-src']  = 'default'
        self.hardDependencies['win32libs-sources/jpeg-src']  = 'default'
        self.hardDependencies['win32libs-sources/libbzip2-src']  = 'default'
        self.hardDependencies['win32libs-sources/libpng-src']  = 'default'
        self.hardDependencies['win32libs-sources/libxml2-src']  = 'default'
        self.hardDependencies['win32libs-sources/libxslt-src']  = 'default'
#        self.hardDependencies['win32libs-sources/openexr-src']  = 'default'
        self.hardDependencies['win32libs-sources/openssl-src']  = 'default'
        self.hardDependencies['win32libs-sources/pcre-src']  = 'default'
        self.hardDependencies['win32libs-sources/shared-mime-info-src']  = 'default'
        self.hardDependencies['win32libs-sources/zlib-src']  = 'default'

        if self.buildTarget == '4.1':
            self.hardDependencies['kdesupport/phonon'] = '4.2.0'
        else:
            self.hardDependencies['kdesupport/phonon'] = '4.3.0'

        self.hardDependencies['kdesupport/qimageblitz'] = 'default'
        self.hardDependencies['kdesupport/soprano'] = 'default'
        self.hardDependencies['kdesupport/strigi'] = 'default'
        self.hardDependencies['data/aspell-data'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        self.buildType = "Debug"
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = " -DKDE4_BUILD_TESTS=OFF "
        if self.compiler == "mingw":
          self.kdeCustomDefines += " -DKDE_DISTRIBUTION_TEXT=\"MinGW 3.4.5\" "
        if self.compiler == "msvc2005":
          self.kdeCustomDefines += " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2005 SP1\" "

        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdelibs-enterprise4", self.buildTarget, True )
        else:
            return self.doPackaging( "kdelibs-enterprise4", os.path.basename(sys.argv[0]).replace("kdelibs-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
