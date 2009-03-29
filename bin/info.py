# this module contains the information class
import datetime
import os

class infoclass:
    def __init__( self, RAW="" ):
        """ """
        self.targets = dict()
        self.targetInstSrc = dict()
        self.svnTargets = dict()
        self.hardDependencies = dict()
        self.softDependencies = dict()
        self.patchToApply = dict()  # list ( 'patchname', patchdepth for patch )
        self.isoDateToday = str( datetime.date.today() ).replace('-', '')
        self.svnTargets['svnHEAD'] = False
        self.svnServer = None       # this will result in the use of the default server (either anonsvn.kde.org or svn.kde.org)
        self.defaultTarget = 'svnHEAD'
        self.buildTarget = 'svnHEAD'
        
        for x in RAW.splitlines():
            if not x == '':
                """ if version is not available then set it as -1 """
                self.hardDependencies[ x ] = [ -1 ]
        

        self.setDependencies()
        self.setTargets()
        self.setSVNTargets()

    def setDependencies( self ):
        """ """

    def setTargets( self ):
        """ """

    def setSVNTargets( self ):
        """ """

    def getPackage( self, repoUrl, name, version ):
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"

        return repoUrl + '/' + name + '-' + compiler + '-' + version + '-bin.tar.bz2\n' + \
               repoUrl + '/' + name + '-' + compiler + '-' + version + '-lib.tar.bz2\n'
