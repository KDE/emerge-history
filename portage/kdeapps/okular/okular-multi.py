import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdegraphics#norecursive;trunk/KDE/kdegraphics/okular;;trunk/KDE/kdegraphics/cmake'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdegraphicslibs'] = 'default'
        self.hardDependencies['win32libs-sources/zlib-src'] = 'default'
        self.hardDependencies['win32libs-sources/poppler-src'] = 'default'
        self.hardDependencies['win32libs-sources/chm-src'] = 'default'
        self.hardDependencies['win32libs-sources/ebook-tools-src'] = 'default'
        self.hardDependencies['win32libs-sources/tiff-src'] = 'default'
        self.hardDependencies['win32libs-sources/djvu-src'] = 'default'
        self.hardDependencies['win32libs-sources/freetype-src'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.onlyBuildTargets='okular'
        self.subinfo.options.configure.defines='-DBUILD_LIBS=Off'

if __name__ == '__main__':
    Package().execute()
