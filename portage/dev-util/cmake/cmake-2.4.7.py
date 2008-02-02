import base
import info

SRC_URI= "http://www.cmake.org/files/v2.4/cmake-2.4.7-win32-x86.zip"

class subinfo( info.infoclass ):
    def setTargets( self ):
        """ """
        self.targets['2.4.7'] = 'http://www.cmake.org/files/v2.4/cmake-2.4.7-win32-x86.zip'
        self.targetInstSrc['2.4.7'] = 'cmake-2.4.7-win32-x86'
        self.defaultTarget = '2.4.7'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, SRC_URI )
    self.instsrcdir = "cmake-2.4.7-win32-x86"
    self.subinfo = subinfo()
    if self.traditional:
      self.instdestdir = "cmake"

if __name__ == '__main__':
    subclass().execute()
