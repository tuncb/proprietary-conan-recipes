from conans import ConanFile
import os

class IntelMklConan(ConanFile):
    name = "intel-tbb"
    version = "2018"
    settings = {
        "os": ["Windows"],
        "arch": ["x86_64"]
    }    
       
    def package_info(self):
        mkl_root = os.environ["ICPP_COMPILER18"]
        self.cpp_info.includedirs = ["{}\\tbb\\include".format(mkl_root)]
        self.cpp_info.libdirs = ["{}\\tbb\\lib\\intel64_win\\vc14".format(mkl_root)]

        self.cpp_info.debug.libs = ["tbb_debug.lib"]
        self.cpp_info.release.libs = ["tbb.lib"]