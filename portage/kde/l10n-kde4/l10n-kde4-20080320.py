import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/l10n-kde4/%s'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'
    

from Package.CMakePackageBase import *

class Package(PackageBase, SvnSource, CMakeBuildSystem, KDEWinPackager):
    def __init__( self  ):
        self.subinfo = subinfo()
        PackageBase.__init__( self )
        SvnSource.__init__( self )
        CMakeBuildSystem.__init__( self )
        KDEWinPackager.__init__( self )
        self.language = 'de'

    def repositoryPath(self):
        # \todo we cannot use CMakePackageBase here because repositoryPath 
        # then is not be overrideable for unknown reasons 
        url = SvnSource.repositoryPath(self) % self.language
        return url

    def sourceDir(self):
        dir = SvnSource.sourceDir(self) % self.language
        return dir
        
    def buildRoot(self):
        dir = os.path.join(PackageBase.buildRoot(self), self.language)
        return dir

    def unpack(self):
        autogen = os.path.join( self.packageDir() , "autogen.py" )
        if not SvnSource.unpack(self): 
            return False
        # execute autogen.py and generate the CMakeLists.txt files
        cmd = "cd %s && python %s %s" % \
              (self.sourceDir()+'/..', autogen, self.language )
        print cmd
        utils.system( cmd )
        return True
        
    def createPackage(self):
        self.subinfo.options.package.packageName = 'l10n-kde4-%s' % self.language
        self.subinfo.options.package.withCompiler = False
        return KDEWinPackager.createPackage(self)
        
        
class MainInfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/l10n-kde4/scripts'
        self.defaultTarget = 'svnHEAD'
        # all targets in svn
        self.languages  = 'af ar be bg bn bn_IN br ca cs csb cy da de '
        self.languages += 'el en_GB eo es et eu fa fi fr fy ga gl gu '
        self.languages += 'ha he hi hr hsb hu hy is it ja ka kk km kn ko ku '
        self.languages += 'lb lt lv mk ml ms mt nb nds ne nl nn nso oc '
        self.languages += 'pa pl pt pt_BR ro ru rw se sk sl sr sv '
        self.languages += 'ta te tg th tr uk uz vi wa xh zh_CN zh_HK zh_TW '

        # released target in 4.0.83
        self.languages  = 'ar be bg ca cs csb da de '
        self.languages += 'el en_GB eo es et eu fa fi fr fy ga gl '
        self.languages += 'hi hu is it ja kk km ko '
        self.languages += 'lv mk nb nds ne nl nn '
        self.languages += 'pa pl pt pt_BR ro ru se sl sv '
        self.languages += 'ta th tr uk wa zh_CN zh_TW '

        #for testing
        self.languages  = 'de'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/cmake'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'
    
    
class MainPackage(PackageBase):
    def __init__( self  ):
        self.subinfo = MainInfo()
        PackageBase.__init__( self )
        self.l10n_kde4 = portage.getPackageInstance('kde','l10n-kde4')

    def execute(self):
        (command, option) = self.getAction()
        ## \todo does not work yet see note in PackageBase::getAction()
        if option <> None:
            languages = option.split()
        else:
            languages = self.subinfo.languages.split()
        for language in languages:
            self.l10n_kde4.language = language
            if not self.l10n_kde4.runAction(command):
                return False
            
        
if __name__ == '__main__':
    MainPackage().execute()

