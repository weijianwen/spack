#!/usr/bin/env python3

from spack_install import install
import os, sys

# Build system with gcc@4.8.5
GCC48 = "gcc@4.8.5"
JDK18 = "jdk@1.8.0_202"

## Install Intel Compiler %intel
for pkg in ["intel-parallel-studio@cluster.2016.4+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(GCC48),
            "intel-parallel-studio@cluster.2017.7+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(GCC48),
            "intel-parallel-studio@cluster.2018.3+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(GCC48),
            "intel-parallel-studio@cluster.2019.2+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(GCC48)
]:
    os.system("rm -f $HOME/spack/etc/spack/licenses/intel/license.lic")
    os.system("rm -f $HOME/intel")
    install(pkg)

## Build Intel Parallel Studio with %intel
for pkg in ["intel-parallel-studio@cluster.2016.4+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@16.0.4 threads=openmp",
            "intel-parallel-studio@cluster.2017.7+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@17.0.7 threads=openmp",
            "intel-parallel-studio@cluster.2018.3+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@18.0.3 threads=openmp",
            "intel-parallel-studio@cluster.2019.2+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@19.0.2 threads=openmp"
]:
    os.system("rm -f $HOME/spack/etc/spack/licenses/intel/license.lic")
    os.system("rm -f $HOME/intel")
    install(pkg)

## Install JDK with
install("{} %{}".format(JDK18, GCC48))

## Install JDK-dependent packages
for pgk in ["maven@3.3.9", "gradle@4.8.1", "ant@1.9.9", "sbt@1.1.6"]:
    install("{} %{} ^{}".format(pgk, GCC48, JDK18))

# Install other system packages against GCC48
for pkg in ["miniconda2@4.5.4",
             "miniconda3@4.5.4",
            "gcc~binutils@4.9.4",
            "gcc~binutils@5.4.0",
            "gcc~binutils@6.4.0",
            "gcc~binutils@7.3.0",
            "gcc~binutils@8.2.0",
            "pgi+nvidia+single~network@18.4",
            "cuda@9.0.176",
            "cuda@8.0.61",
            "cuda@7.5.18",
            "cuda@6.5.14",
            "cudnn@7.0",
            "cudnn@6.0",
            "cudnn@5.1"
]:
    install("{} %{}".format(pkg, GCC48))

# Build non-MPI packages
for pkg in {}.items():
    install(pkg)

# Build MPI libraries
for pkg in ["openmpi@3.1.3+legacylaunchers+pmi~cuda %gcc@8.3.0 fabrics=verbs schedulers=slurm",
            "mvapich2@2.3~cuda %gcc@8.3.0 fabrics=mrail file_systems=lustre process_managers=slurm",
            "openmpi@3.1.3+legacylaunchers+pmi~cuda %intel@19.0.2 fabrics=verbs schedulers=slurm",
            "mvapich2@2.3~cuda %intel@19.0.2 fabrics=mrail file_systems=lustre process_managers=slurm"
        # "mvapich2@2.3~cuda fabrics={} process_managers=slurm file_systems=lustre".format(MVFAB): "",
        # "mvapich2@2.3+cuda fabrics={} process_managers=slurm file_systems=lustre".format(MVFAB): "^cuda@8.0.61",
        # "mpich@3.2.1+pmi+hydra+romio+verbs": "",
        # "intel-parallel-studio@cluster.2018.1+mpi": ""
]:
    install(pkg)

# Build MPI-depedent packages
for pkg in []:
    install(pkg)

# Remove intermediate dependency
for pkg in ["gperf", "inputproto", "help2man", "nasm"]:
    os.system("spack uninstall -y --all {}".format(pkg))
