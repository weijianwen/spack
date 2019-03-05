#!/usr/bin/env python3

from spack_install import install
from spack_install import check_pass
import os, sys

if len(sys.argv) > 1:
          PLATFORM = sys.argv[1]
else:
          PLATFORM = sandybridge


# Build system with gcc@4.8.5
GCC48 = "gcc@4.8.5"
JDK18 = "jdk@1.8.0_202"

## Install Intel Compiler %intel
for pkg in ["intel-parallel-studio@cluster.2016.4+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(GCC48),
            "intel-parallel-studio@cluster.2017.7+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(GCC48),
            "intel-parallel-studio@cluster.2018.3+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(GCC48),
            "intel-parallel-studio@cluster.2019.2+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(GCC48)]:
    os.system("rm -f $HOME/spack/etc/spack/licenses/intel/license.lic")
    install(pkg)

## Build Intel Parallel Studio with %intel
for pkg in ["intel-parallel-studio@cluster.2016.4+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@16.0.4 threads=openmp",
            "intel-parallel-studio@cluster.2017.7+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@17.0.7 threads=openmp",
            "intel-parallel-studio@cluster.2018.3+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@18.0.3 threads=openmp",
            "intel-parallel-studio@cluster.2019.2+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@19.0.2 threads=openmp"]:
    os.system("rm -f $HOME/spack/etc/spack/licenses/intel/license.lic")
    install(pkg)

## Install JDK with
install("{} %{}".format(JDK18, GCC48))

## Install JDK-dependent packages
for pgk in ["maven@3.3.9", "gradle@4.8.1", "ant@1.9.9", "sbt@1.1.6"]:
    install("{} %{} ^{}".format(pgk, GCC48, JDK18))

# Install other system packages against GCC48
packages = {"miniconda2@4.5.4": [""],
            "miniconda3@4.5.4": [""],
            "gcc~binutils@4.9.4": [""],
            "gcc~binutils@5.4.0": [""],
            "gcc~binutils@6.4.0": [""],
            "gcc~binutils@7.3.0": [""],
            "gcc~binutils@8.2.0": [""],
            "pgi+nvidia+single~network@18.4": [""],
            "cuda@9.0.176": [""],
            "cuda@8.0.61": [""],
            "cuda@7.5.18": [""],
            "cuda@6.5.14": [""],
            "cudnn@7.0": ["^cuda@9.0.176", "^cuda@8.0.61"],
            "cudnn@6.0": ["^cuda@8.0.61"],
            "cudnn@5.1": ["^cuda@8.0.61"]
}
for pkg,specs in packages.items():
    for spec in specs:
          install("{} %{} {}".format(pkg, GCC48, spec))


COMPILERS = ["gcc@8.2.0", "intel@19.0.2"]

# Build non-MPI packages
nonmpipkgs = {}
for pkg,specs in nonmpipkgs.items():
    for spec in specs:
        for cc in COMPILERS:
                if check_pass(pkg, cc, spec, PLATFORM):
                    install("{} %{} {}".format(pkg, cc, spec))

# Build MPI library
if os.system("lspci | grep Omni-Path") == 0:
    MVFAB = "psm"
    OMPIFAB = "psm2"
elif os.system("lspci | grep Mellanox") == 0:
    MVFAB = "mrail"
    OMPIFAB = "verbs"
else:
    MVFAB = ""
    OMPIFAB = ""

# Build MPI libraries
MPIS = {"openmpi@3.1.0+pmi~vt~cuda fabrics={} ~java schedulers=slurm".format(OMPIFAB): "",
        "mvapich2@2.3~cuda fabrics={} process_managers=slurm file_systems=lustre".format(MVFAB): "",
        # "mvapich2@2.3+cuda fabrics={} process_managers=slurm file_systems=lustre".format(MVFAB): "^cuda@8.0.61",
        "mpich@3.2.1+pmi+hydra+romio+verbs": ""
}
for pkg,spec in MPIS.items():
    for cc in COMPILERS:
        if 'intel-parallel' not in pkg:
                if check_pass(pkg, cc, spec, PLATFORM):
                          install("{} %{} {}".format(pkg, cc, spec))

## Build MPI packages
mpipkgs = {}
for pkg,specs in mpipkgs.items():
    for spec in specs:
        for cc in COMPILERS:
            for mpi in MPIS.keys():
                if spec == "":
                   concrete_spec = "{} %{} ^{}".format(pkg, cc, mpi)
                else:
                   concrete_spec = "{} %{} {} ^{}".format(pkg, cc, spec, mpi)
                if check_pass(pkg, cc, spec, mpi, PLATFORM):
                    install(concrete_spec)

## Remove intermediate dependency
for pkg in ["gperf", "inputproto", "help2man", "nasm"]:
    os.system("spack uninstall -y --all {}".format(pkg))

## Remove intermediate dependency
for pkg in ["perl"]:
    os.system("spack uninstall -y {}".format(pkg))
