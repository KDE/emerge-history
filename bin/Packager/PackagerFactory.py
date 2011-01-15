#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from Packager.KDEWinPackager import *
from Packager.CPackPackager import *
from Packager.SevenZipPackager import *
from Packager.MSInstallerPackager import *
from Packager.InnoSetupPackager import *

def init(packager, parent):
    packager.subinfo = parent.subinfo
    packager.parent = parent
    packager.category = parent.category
    packager.package = parent.package
    packager.version = parent.version
    packager.buildTarget = parent.subinfo.buildTarget
    packager.PV = parent.PV
    return

def PackagerFactory(parent, packagerType):
    """provides multi packager type api
    return PackagerBase derived instance for recent settings"""
    utils.debug( "PackagerFactory called", 2 )
    packager = None
    packagers = []

    if packagerType != None:
        # TODO: simplify
        if 'KDEWin' in packagerType or 'kdewin' in packagerType:
            packager = KDEWinPackager()
            init(packager, parent)
            packagers.append(packager)

        if 'CPack' in packagerType:
            packager = CPackPackager()
            init(packager, parent)
            packagers.append(packager)

        if '7z' in packagerType:
            packager = SevenZipPackager()
            init(packager, parent)
            packagers.append(packager)

        if 'Inno' in packagerType or 'inno' in packagerType:
            packager = InnoSetupPackager()
            init(packager, parent)
            packagers.append(packager)

        if packager == None:
            utils.die("none or unsupported packager set, use self.packagerType='type', where type could be 'KDEWin'")
        return packagers
    else:
        # automatic detection
        packager = InnoSetupPackager()
        init(packager, parent)

        if packager.configFile() != None:
            packagers.append(packager)

        # default packager
        if len(packagers) == 0:
            packager = KDEWinPackager()
            init(packager, parent)
            packagers.append(packager)

        return packagers

