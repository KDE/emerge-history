import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.targets['2.0.0-5'] = 'http://delta.affinix.com/download/qca/2.0/qca-2.0.0.tar.bz2'
        self.targetInstSrc['2.0.0-5'] = 'qca-2.0.0'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qca'
        self.defaultTarget = 'svnHEAD'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "qca"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == "svnHEAD":
            self.instdestdir = "kde"
            return self.doPackaging( "qca", os.path.basename(sys.argv[0]).replace("qca-", ""), True )
        else:
            return self.doPackaging( "qca", self.buildTarget, True )
if __name__ == '__main__':
    subclass().execute()
