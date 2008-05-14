import base
import os
import shutil
import re
import utils
import info

# #########################################################################################
# ATTENTION: currently the only libraries that are built are boost.python libs
# that implies that the bin package requires the lib package as well to be used for compilation
# #########################################################################################

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.34.1'] = 'http://downloads.sourceforge.net/boost/boost_1_34_1.tar.bz2'
        self.targetInstSrc['1.34.1'] = 'boost_1_34_1'
        self.targets['1.35.0'] = 'http://downloads.sourceforge.net/boost/boost_1_35_0.tar.bz2'
        self.targetInstSrc['1.35.0'] = 'boost_1_35_0'
        self.defaultTarget = '1.35.0'
    
    def setDependencies( self ):
        self.hardDependencies['dev-util/win32libs'] = 'default'
        self.hardDependencies['dev-util/bjam'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        #self.createCombinedPackage = True  # no longer true :(
        if self.compiler == "mingw":
            self.toolset = "gcc"
        else:
            self.toolset = "msvc"
        self.subinfo = subinfo()

    def execute( self ):
        base.baseclass.execute( self )

    def compile( self ):
        """"""
        cmd = "cd %s && bjam --toolset=%s --prefix=%s --with-python --layout=system" % ( os.path.join( self.workdir, self.instsrcdir ),
        self.toolset, os.path.join( self.workdir, self.imagedir ))
        if utils.verbose() >= 1:
            print cmd
        os.system( cmd ) and utils.die( "compile failed because of this cobbled stuff: %s" % ( cmd ) )
        return True

    def install( self ):
        """"""
        cmd = "cd %s && bjam --toolset=%s --prefix=%s --with-python --layout=system install" % ( os.path.join( self.workdir, self.instsrcdir ),
        self.toolset, os.path.join( self.workdir, self.imagedir ))
        if utils.verbose() >= 1:
            print cmd
        os.system( cmd ) and utils.die( "compile failed because of this cobbled stuff: %s" % ( cmd ) )

        # copy runtime libraries to the bin folder
        cmd = "cd %s && mkdir bin && copy lib\\*.dll bin" % ( os.path.join( self.workdir, self.imagedir ) )
        if utils.verbose() >= 1:
            print cmd
        os.system( cmd ) and utils.die( "compile failed because of this cobbled stuff: %s" % ( cmd ) )
        return True

    def make_package( self ):
        return self.doPackaging( "boost", "boost_" + self.buildTarget.replace('.','_') , True )

if __name__ == '__main__':
    subclass().execute()
