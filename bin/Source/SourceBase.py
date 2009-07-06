# -*- coding: utf-8 -*-

from EmergeBase import *

class SourceBase(EmergeBase):
    """ implements basic stuff required for  all sources"""
    url = ""
    def __init__(self):
        EmergeBase.__init__(self)

    def fetch(self): abstract()

    def unpack(self): abstract()

    # return source dir 
    def sourceDir(self): abstract()

    def applyPatches(self):
        """ apply patches is available """
        utils.debug( "SourceBase.applyPatches called", 1 )

        if self.subinfo.hasTarget():
            ( file, patchdepth ) = self.subinfo.patchesToApply()
            if file:
                patchfile = os.path.join ( self.packagedir, file )
                srcdir = os.path.join ( self.workDir(), self.instsrcdir )
                return utils.applyPatch( patchfile, srcdir, patchdepth )
        return True

