import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base']            = 'default'
        self.hardDependencies['libs/qt']               = 'default'
        self.hardDependencies['kdesupport/clucene-core'] = 'default'
        self.hardDependencies['win32libs-bin/redland']   = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/soprano'
        self.svnTargets['2.0.0']  = 'tags/soprano/2.0.0'
        self.svnTargets['2.0.1']  = 'tags/soprano/2.0.1'
        self.svnTargets['2.0.2']  = 'tags/soprano/2.0.2'
        self.svnTargets['2.0.3']  = 'tags/soprano/2.0.3'
        self.svnTargets['2.0.99'] = 'tags/soprano/2.0.99'
        self.svnTargets['2.1']    = 'tags/soprano/2.1'
        self.svnTargets['2.1.1']  = 'tags/soprano/2.1.1'
        self.svnTargets['2.1.64'] = 'tags/soprano/2.1.64'
        self.svnTargets['2.1.65'] = 'tags/soprano/2.1.65'
        self.svnTargets['2.1.67'] = 'tags/soprano/2.1.67'
        self.svnTargets['2.2']    = 'tags/soprano/2.2'
        self.svnTargets['2.2.1']  = 'tags/soprano/2.2.1'
        self.svnTargets['2.2.2']  = 'tags/soprano/2.2.2'
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdesupport/soprano'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdesupport/soprano'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdesupport/soprano'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdesupport/soprano'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdesupport/soprano'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdesupport/soprano'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdesupport/soprano'
        self.defaultTarget = '20100129'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "soprano"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "soprano", self.buildTarget, True )
        else:
            return self.doPackaging( "soprano", utils.cleanPackageName( sys.argv[0], "soprano" ), True )

if __name__ == '__main__':
    subclass().execute()
