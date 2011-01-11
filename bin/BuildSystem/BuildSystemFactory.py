# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from KDE4BuildSystem import *
from CMakeBuildSystem import *
from QMakeBuildSystem import *
from AutoToolsBuildSystem import *
from BinaryBuildSystem import *

import info
import utils

def BuildSystemFactory(buildSystemType, source):
    """ return BuildSystemBase derived instance for recent settings"""
    utils.debug( "buildsystemFactory called for type %s" % buildSystemType, 1 )
    buildSystem = None

    if buildSystemType == None or buildSystemType == 'cmake':
        buildSystem = CMakeBuildSystem()
    elif buildSystemType == 'kde4':
        buildSystem = KDE4BuildSystem()
    elif buildSystemType == 'qmake':
        buildSystem = QMakeBuildSystem()
    elif buildSystemType == 'autotools':
        buildSystem = AutoToolsBuildSystem()
    elif buildSystemType == 'binary':
        buildSystem = BinaryBuildSystem()
    else:   
        utils.die("none or unsupported buildsystem set, use self.buildSystemType='type', where type could be 'binary', 'cmake', 'qmake', 'autotools' or 'KDE4'")
        
    buildSystem.source = source
    buildSystem.subinfo = source.subinfo
    # for cleanimage
    buildSystem.type  = buildSystemType
    # required for archive source
    source.buildSystemType = buildSystemType
    return buildSystem
