import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.1/kdebase/workspace'
        for ver in ['0', '1', '2', '3']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.1.' + ver + '/src/kdebase-workspace-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdebase-workspace-4.1.' + ver
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde-4.1/kdelibs'] = 'default'
        self.hardDependencies['kde-4.1/kdepimlibs'] = 'default'
        self.hardDependencies['kde-4.1/kdebase-runtime'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "workspace"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = ""
        self.kdeCustomDefines += " -DBUILD_libs=OFF"
        self.kdeCustomDefines += " -DBUILD_systemsettings=OFF"
        self.kdeCustomDefines += " -DBUILD_kcheckpass=OFF"
        self.kdeCustomDefines += " -DBUILD_kscreensaver=OFF"
        self.kdeCustomDefines += " -DBUILD_solid=OFF"
        self.kdeCustomDefines += " -DBUILD_ksmserver=OFF"
        self.kdeCustomDefines += " -DBUILD_kcminit=OFF"
        self.kdeCustomDefines += " -DBUILD_ksplash=OFF"
        self.kdeCustomDefines += " -DBUILD_ksysguard=OFF"
        self.kdeCustomDefines += " -DBUILD_klipper=OFF"
        self.kdeCustomDefines += " -DBUILD_kmenuedit=OFF"
        self.kdeCustomDefines += " -DBUILD_krunner=OFF"
        self.kdeCustomDefines += " -DBUILD_kwin=OFF"
        self.kdeCustomDefines += " -DBUILD_printer-applet=OFF"
        self.kdeCustomDefines += " -DBUILD_kstartupconfig=OFF"
        self.kdeCustomDefines += " -DBUILD_khotkeys=OFF"
        self.kdeCustomDefines += " -DBUILD_kcontrol=OFF"
        self.kdeCustomDefines += " -DBUILD_ksystraycmd=OFF"
#        self.kdeCustomDefines += " -DBUILD_plasma=OFF"
#        self.kdeCustomDefines += " -DBUILD_doc=OFF"
#        self.kdeCustomDefines += " -DBUILD_wallpapers=OFF"

        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdebase-workspace", self.buildTarget, True )
        else:
            return self.doPackaging( "kdebase-workspace", os.path.basename(sys.argv[0]).replace("kdebase-workspace-", "").replace(".py", ""), True )


if __name__ == '__main__':
    subclass().execute()
