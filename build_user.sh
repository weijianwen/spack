#!/usr/bin/env python3

from spack_install import install
import os

# Register exernal packages
for pkg in ["jdk@1.8.0_181-b13%gcc@4.8.5",
            "jdk@1.8.0_202%gcc@4.8.5",
            "gcc@8.3.0%gcc@4.8.5",
            "gcc@7.3.0%gcc@4.8.5",
            "gcc@6.4.0%gcc@4.8.5",
            "gcc@5.4.0%gcc@4.8.5",
            "gcc@4.9.4%gcc@4.8.5",
            "environment-modules@3.2.10",
            "intel-parallel-studio@cluster.2016.4+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@16.0.4 threads=openmp",
            "intel-parallel-studio@cluster.2017.7+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@17.0.7 threads=openmp",
            "intel-parallel-studio@cluster.2017.5+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@17.0.5 threads=openmp",
            "intel-parallel-studio@cluster.2018.1+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@18.0.1 threads=openmp",
            "intel-parallel-studio@cluster.2018.3+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@18.0.3 threads=openmp",
            "intel-parallel-studio@cluster.2019.2+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@19.0.2 threads=openmp"]:
           os.system("spack install {}".format(pkg))
