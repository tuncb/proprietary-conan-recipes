from conans import ConanFile
import os

class MsmpiConan(ConanFile):
    name = "msmpi"
    version = "2008.2"
    settings = {
        "os": ["Windows"],
        "arch": ["x86", "x86_64"],
    }    

    def package_info(self):
        self.cpp_info.includedirs = [os.environ["MSMPI_INC"]]
        self.cpp_info.libs = ["msmpi"]
        if self.settings.arch == "x86":
            self.cpp_info.libdirs = [os.environ["MSMPI_LIB32"]]
        else:
            self.cpp_info.libdirs = [os.environ["MSMPI_LIB64"]]
