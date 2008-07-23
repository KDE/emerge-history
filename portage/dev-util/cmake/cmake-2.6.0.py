import base
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['2.4.8'] = 'http://www.cmake.org/files/v2.4/cmake-2.4.8-win32-x86.zip'
        self.targets['2.6.0'] = 'http://www.cmake.org/files/v2.6/cmake-2.6.0-win32-x86.zip'
        self.targets['2.6.1'] = 'http://www.cmake.org/files/v2.6/cmake-2.6.1-RC-11-win32-x86.zip'
        self.targetInstSrc['2.4.8'] = 'cmake-2.4.8-win32-x86'
        self.targetInstSrc['2.6.0'] = 'cmake-2.6.0-win32-x86'
        self.targetInstSrc['2.6.1'] = 'cmake-2.6.1-RC-11-win32-x86'
        self.defaultTarget = '2.6.0'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.subinfo = subinfo()
    if self.traditional:
      self.instdestdir = "cmake"

if __name__ == '__main__':
    subclass().execute()
