from Package.CMakePackageBase import *
import info
import shutil
import os
import re
import urllib
import emergePlatform

# currently only needed from kdenetwork


class subinfo(info.infoclass):
    def setTargets( self ):
        self.baseURL = "http://artfiles.org/mysql/Downloads/MySQL-5.1/"
        if( emergePlatform.buildArchitecture() == 'x64' ):
          self.targets[ '5.1.54'] = self.baseURL+"mysql-noinstall-5.1.54-winx64.zip"
          self.targetInstSrc[ '5.1.54' ] = "mysql-5.1.54-winx64"
          self.targetDigests[ '5.1.54' ] = 'e9376cfb93f4b0b735f1949395fe1e1463c3050d'
        else:
          self.targets[ '5.1.54'] = self.baseURL+"mysql-noinstall-5.1.54-win32.zip"
          self.targetInstSrc[ '5.1.54' ] = "mysql-5.1.54-win32"
          self.targetDigests['5.1.54'] = '2c4ae53b1f7e97572482edac8bd82c5443771302'
        self.shortDescription = "MySql database server and embedded library"
        self.options.package.withCompiler = False
        self.defaultTarget = '5.1.54'


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


class Package(CMakePackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    self.subinfo.options.merge.ignoreBuildType = True
    self.subinfo.options.package.packSources = False
    CMakePackageBase.__init__( self )


  def compile( self ):
    return True

  def install( self ):
    if( not self.cleanImage()):
      return False
    shutil.copytree( os.path.join( self.sourceDir() , "bin" ) , os.path.join( self.installDir(), "bin") , ignore=shutil.ignore_patterns('*.pdb','*.map','*test.exe','mysqld-debug.exe') )
    # do not create lib files, just take the given ones, because of the stdcall problem
    os.mkdir( os.path.join( self.installDir(), "lib"  ) )
    shutil.copy( os.path.join( self.sourceDir() , "lib" , "opt" , "libmysql.lib" ) , os.path.join( self.installDir(), "lib" , "libmysql.lib" ) )
    os.mkdir(os.path.join( self.installDir(), "lib" , "plugin"))
    shutil.copy( os.path.join( self.sourceDir() , "lib" , "plugin" , "ha_innodb_plugin.dll" ) , os.path.join( self.installDir(), "lib" , "plugin" , "ha_innodb_plugin.dll" ) )
    shutil.copy( os.path.join( self.sourceDir() , "Embedded" , "DLL" , "release" , "libmysqld.dll" ) , os.path.join( self.installDir(), "bin" , "libmysqld.dll" ) )
    shutil.copy( os.path.join( self.sourceDir() , "Embedded" , "DLL" , "release" , "libmysqld.lib" ) , os.path.join( self.installDir(), "lib" , "libmysqld.lib" ) )
    shutil.copytree( os.path.join( self.sourceDir() , "include" ) , os.path.join( self.installDir(), "include" ) ,  ignore=shutil.ignore_patterns('*.def') )
    shutil.copytree( os.path.join( self.sourceDir() , "scripts" ) , os.path.join( self.installDir(), "scripts" ) )
    shutil.copytree( os.path.join( self.sourceDir() , "share" ) , os.path.join( self.installDir(), "share" ) , ignore=shutil.ignore_patterns('Makefile*') )
    shutil.copytree( os.path.join( self.sourceDir() , "data" ) , os.path.join( self.installDir(), "data" ) )

    return True

if __name__ == '__main__':
    Package().execute()
