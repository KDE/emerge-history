#!/usr/bin/env python

"""
    provides shells     
"""

import os
import utils
import sys
import compiler
import compilercache

## \todo requires installed msys package -> add suport for installing packages 

class Shell(object):
    def __init__(self):
        dummy = 0

    #""" convert internal used paths to native path which are understandable by the shell
    def toNativePath( self, path ): abstract

    #""" execute shell command
    def execute(self, path, cmd, args): abstract
    

class MSysShell(Shell):
    def __init__(self):
        Shell.__init__(self)
        env = dict( os.environ )
        self.msysdir = env[ "MSYSDIR" ]
        self.initEnvironment()
        
    
    def initEnvironment(self,cflags="", ldflags=""):
        self.buildType = os.getenv("EMERGE_BUILDTYPE")
        if compiler.isMinGW():
            compilercache.getMsysMakeArguments()
            if self.buildType == "RelWithDebInfo": 
                cflags += " -O2 -g "
            elif self.buildType == "Debug":
                cflags += " -O0 -g3 "
        elif compiler.isMSVC():
            utils.putenv("LD", "link.exe")
        
        utils.putenv("CFLAGS",cflags)
        utils.putenv("LDFLAGS",ldflags)
        #unset make to remove things like jom
        os.unsetenv("MAKE")
        utils.putenv("PATH" , "%s;%s" %  ( os.environ.get( "PATH" ) , os.path.join( os.environ.get( "KDEROOT" ) , "dev-utils" , "bin" )))
        #seting perl to prevent msys from using msys-perl
        perl = self.toNativePath(os.path.join( os.environ.get( "KDEROOT" ) , "dev-utils" , "bin" , "perl.exe" ))
        utils.putenv("PERL",perl)
        utils.putenv("INTLTOOL_PERL",perl)
        
        #prepare path to sue autotools
        utils.putenv("PATH" , "%s;%s" %  ( os.environ.get( "PATH" ) , os.path.join( os.environ.get( "MSYSDIR" ) , "opt" , "autotools" , "bin" )))
        

    def toNativePath( self, path ):
        path = path.replace( '\\', '/' )
        if ( path[1] == ':' ):
            path = '/' + path[0].lower() + '/' + path[3:]
        return path

    def execute( self, path, cmd, args = "", out=sys.stdout, err=sys.stderr, debugLvl=1 ):
        sh = os.path.join( self.msysdir, "bin", "sh.exe" )

        command = "%s --login -c \"cd %s && %s %s" % \
              ( sh, self.toNativePath( path ), self.toNativePath( cmd ), args )

        command +="\""
        if debugLvl == 0:
            print "%s %s" %(cmd , args)
        else:
            utils.debug( "msys execute: %s" % command, debugLvl )
        return utils.system( command, outstream=out, errstream=err )
       