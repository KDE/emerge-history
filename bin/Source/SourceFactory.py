#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

import info
import utils

from FileSource import *
from ArchiveSource import *
from SvnSource import *
from GitSource import *
from CvsSource import *
from HgSource import *

def SourceFactory(settings):
    """ return sourceBase derived instance for recent settings"""
    utils.trace( "SourceFactory called", 1 )
    source = None

    if settings.hasTarget():
        url = settings.target()
        if url.startswith("[archive]"):
            source = ArchiveSource()
        elif url.find(".exe") != -1 or url.find(".bat") != -1 or url.find(".msi") != -1:
            source = FileSource(settings)
        else:
            source = ArchiveSource(settings)

    ## \todo move settings access into info class
    if settings.hasSvnTarget():
        url = settings.svnTarget()
        sourceType = utils.getVCSType( url )
        if sourceType == "svn":
            source = SvnSource(settings)
        elif sourceType == "hg":
            source = HgSource(settings)
        elif sourceType == "git":
            source = GitSource(settings)
        ## \todo complete more cvs access schemes
        elif sourceType == "cvs":
            source = CvsSource(settings)

    if source == None:
        utils.die("none or unsupported source system set")
    if not source.subinfo:
        source.subinfo = settings
    source.url = url
    return source
