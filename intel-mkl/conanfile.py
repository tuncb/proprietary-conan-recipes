from conans import ConanFile
import os

class IntelMklConan(ConanFile):
    name = "intel-mkl"
    version = "2018"
    settings = {
        "os": ["Windows"],
        "arch": ["x86_64"]
    }    
    options = {
        "shared": [True, False], 
        "threading": ["sequential", "openmp", "tbb"],
        "interface": ["int32", "int64"],
        "mpi": ["msmpi", "intelmpi", "mpich2"],
        "cluster_pardiso": [True, False],
        "cdft": [True, False],
        "scalapack": [True, False],
        "blacs": [True, False],
		"fortran": [True, False],
    }
    default_options = "shared=False", "threading=sequential", "interface=int32", "mpi=msmpi", "cluster_pardiso=False", "cdft=False", "scalapack=False", "blacs=False", "fortran=False"
    
    def get_mkl_core_library(self):
        return "mkl_core{}".format(self.lib_suffix)

    def get_interface_library(self):
        return "mkl_intel_{}{}".format(self.interface_name, self.lib_suffix)

    def get_threading_library(self):
        if self.options.threading == "sequential":
            return "mkl_sequential{}".format(self.lib_suffix)
        elif self.options.threading == "openmp":
            return "mkl_intel_thread{}".format(self.lib_suffix)
        elif self.options.threading == "tbb":
            return "mkl_tbb_thread{}".format(self.lib_suffix)
    
    def add_blacs_if_needed(self, libs):
        is_blacs_needed = (
            self.options.blacs == True or 
            self.options.blacs == True or 
            self.options.blacs == True or 
            self.options.blacs == True
        )
        
        if not is_blacs_needed:
            return
        
        if self.options.shared == True:
            libs.append("mkl_blacs_{}{}".format(self.interface_name, self.lib_suffix))
        else:
            libs.append("mkl_blacs_{}_{}".format(self.options.mpi, self.interface_name))

    def add_scalapack_if_needed(self, libs):
        if self.options.scalapack == True:
            libs.append("mkl_scalapack_{}{}".format(self.interface_name, self.lib_suffix))

    def add_cdft_if_needed(self, libs):
        if self.options.cdft == True:
            libs.append("mkl_cdft_core{}".format(self.lib_suffix))  

    def add_openmp_if_needed(self, libs):
        if self.options.threading == "openmp":
            libs.append("libiomp5md") 

    def find_root_folder(self):
        keys = ["ICPP_COMPILER18", "IFORT_COMPILER18"]
        for key in keys:
            if os.environ.get(key) != None:
                return os.environ[key]
        
        raise Exception('Could not determine intel mkl root.')
    
    def package_info(self):
        root = self.find_root_folder()
        self.cpp_info.includedirs = ["{}\\mkl\\include".format(root)]
        self.cpp_info.libdirs = ["{}\\mkl\\lib\\intel64_win".format(root)]
        if self.options.fortran == True:
            self.cpp_info.libdirs.append("{}\\compiler\\lib\\intel64_win".format(root))

        self.lib_suffix = "" if self.options.shared == False else "_dll"
        self.interface_name = "ilp64" if self.options.interface == "int64" else "lp64"

        libs = [self.get_mkl_core_library(), self.get_threading_library(), self.get_interface_library()]
        self.add_blacs_if_needed(libs)
        self.add_cdft_if_needed(libs)
        self.add_scalapack_if_needed(libs)
        self.add_openmp_if_needed(libs)

        self.cpp_info.libs = libs