import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['4.2'] = 'http://www.docbook.org/xml/4.2/docbook-xml-4.2.zip'
        self.targetDigests['4.2'] = '5e3a35663cd028c5c5fbb959c3858fec2d7f8b9e'
        self.targets['4.5'] = 'http://www.docbook.org/xml/4.5/docbook-xml-4.5.zip'
        self.shortDescription = "document type definition for docbook format"
        self.options.package.withCompiler = False
        self.options.package.packSources = False
        self.defaultTarget = '4.2'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        self.subinfo.options.install.installPath = 'share/xml/docbook/schema/dtd/%s' % self.subinfo.buildTarget

if __name__ == '__main__':
    Package().execute()
