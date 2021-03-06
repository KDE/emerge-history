# -*- coding: utf-8 -*-
import base
import utils
import sys
import os
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/automoc'] = 'default'
        self.dependencies['enterprise5/soprano-e5'] = 'default'
        self.dependencies['win32libs-bin/boost'] = 'default'
        self.dependencies['win32libs-bin/libxslt'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['win32libs-bin/sqlite'] = 'default'
        self.dependencies['win32libs-bin/shared-mime-info'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:akonadi.git'
        self.svnTargets['0.80'] = 'tags/akonadi/0.80'
        self.svnTargets['0.81'] = 'tags/akonadi/0.81'
        self.svnTargets['0.82'] = 'tags/akonadi/0.82'
        self.svnTargets['1.0.0'] = 'tags/akonadi/1.0.0'
        self.svnTargets['1.0.80'] = 'tags/akonadi/1.0.80'
        self.svnTargets['1.1.0']  = 'tags/akonadi/1.1.0'
        self.svnTargets['1.1.1']  = 'tags/akonadi/1.1.1'
        self.svnTargets['1.1.2']  = 'tags/akonadi/1.1.2'
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdesupport/akonadi'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdesupport/akonadi'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdesupport/akonadi'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdesupport/akonadi'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdesupport/akonadi'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdesupport/akonadi'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdesupport/akonadi'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdesupport/akonadi'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdesupport/akonadi'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/kdesupport/akonadi'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/kdesupport/akonadi'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/kdesupport/akonadi'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/kdesupport/akonadi'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/kdesupport/akonadi'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/kdesupport/akonadi'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/kdesupport/akonadi'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/kdesupport/akonadi'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/kdesupport/akonadi'
        self.svnTargets['20100528'] = 'tags/kdepim/enterprise5.0.20100528.1131643/kdesupport/akonadi'
        self.svnTargets['20100604'] = 'tags/kdepim/enterprise5.0.20100604.1134428/kdesupport/akonadi'
        self.svnTargets['20100611'] = 'tags/kdepim/enterprise5.0.20100611.1136974/kdesupport/akonadi'
        self.svnTargets['20100618'] = 'tags/kdepim/enterprise5.0.20100618.1139547/kdesupport/akonadi'
        self.svnTargets['20100625'] = 'tags/kdepim/enterprise5.0.20100625.1142603/kdesupport/akonadi'
        self.svnTargets['20100701'] = 'tags/kdepim/enterprise5.0.20100701.1144979/kdesupport/akonadi'
        self.svnTargets['20100709'] = 'tags/kdepim/enterprise5.0.20100709.1148001/kdesupport/akonadi'
        self.svnTargets['20100716'] = 'tags/kdepim/enterprise5.0.20100716.1150616/kdesupport/akonadi'
        self.svnTargets['20100723'] = 'tags/kdepim/enterprise5.0.20100723.1153624/kdesupport/akonadi'
        self.svnTargets['20100730'] = 'tags/kdepim/enterprise5.0.20100730.1157241/kdesupport/akonadi'
        self.svnTargets['20100805'] = 'tags/kdepim/enterprise5.0.20100805.1159431/kdesupport/akonadi'
        self.svnTargets['20100813'] = 'tags/kdepim/enterprise5.0.20100813.1163234/kdesupport/akonadi'
        self.svnTargets['20100820'] = 'tags/kdepim/enterprise5.0.20100820.1165957/kdesupport/akonadi'
        self.svnTargets['20100827'] = 'tags/kdepim/enterprise5.0.20100827.1168749/kdesupport/akonadi'
        self.svnTargets['20100903'] = 'tags/kdepim/enterprise5.0.20100903.1171282/kdesupport/akonadi'
        self.svnTargets['20100910'] = 'tags/kdepim/enterprise5.0.20100910.1173808/kdesupport/akonadi'
        self.svnTargets['20100917'] = 'tags/kdepim/enterprise5.0.20100917.1176291/kdesupport/akonadi'
        self.svnTargets['20100927'] = 'tags/kdepim/enterprise5.0.20100927.1180225/kdesupport/akonadi'
        self.svnTargets['20101001'] = 'tags/kdepim/enterprise5.0.20101001.1181557/kdesupport/akonadi'
        self.svnTargets['20101008'] = 'tags/kdepim/enterprise5.0.20101008.1183806/kdesupport/akonadi'
        self.svnTargets['20101015'] = 'tags/kdepim/enterprise5.0.20101015.1186246/kdesupport/akonadi'
        self.svnTargets['20101022'] = 'tags/kdepim/enterprise5.0.20101022.1188481/kdesupport/akonadi'
        self.defaultTarget = 'gitHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = (
                " -DINSTALL_QSQLITE_IN_QT_PREFIX=TRUE"
                " -DDATABASE_BACKEND=SQLITE " )

if __name__ == '__main__':
    Package().execute()
