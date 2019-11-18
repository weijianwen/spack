# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os
import sys


class Julia(Package):
    """The Julia Language: A fresh approach to technical computing"""

    homepage = "http://julialang.org"
    url      = "https://github.com/JuliaLang/julia/releases/download/v0.4.3/julia-0.4.3-full.tar.gz"
    git      = "https://github.com/JuliaLang/julia.git"

    version('master', branch='master')
    version('1.1.1',  sha256='3c5395dd3419ebb82d57bcc49dc729df3b225b9094e74376f8c649ee35ed79c2')
    version('1.0.0', sha256='1a2497977b1d43bb821a5b7475b4054b29938baae8170881c6b8dd4099d133f1')
    version('0.6.2', sha256='1e34c13091c9ddb47cf87a51566d94a06613f3db3c483b8f63b276e416dd621b')
    version('release-0.5', branch='release-0.5')
    version('0.5.2', sha256='f5ef56d79ed55eacba9fe968bb175317be3f61668ef93e747d76607678cc01dd')
    version('0.5.1', sha256='533b6427a1b01bd38ea0601f58a32d15bf403f491b8415e9ce4305b8bc83bb21')
    version('0.5.0', sha256='732478536b6dccecbf56e541eef0aed04de0e6d63ae631b136e033dda2e418a9')
    version('release-0.4', branch='release-0.4')
    version('0.4.7', sha256='d658d5bd5fb79b19f3c01cadb9aba8622ca8a12a4b687acc7d99c21413623570')
    version('0.4.6', sha256='4c23c9fc72398014bd39327c2f7efd3a301884567d4cb2a89105c984d4d633ba')
    version('0.4.5', sha256='cbf361c23a77e7647040e8070371691083e92aa93c8a318afcc495ad1c3a71d9')
    version('0.4.3', sha256='2b9df25a8f58df8e43038ec30bae195dfb160abdf925f3fa193b59d40e4113c5')

    # TODO: Split these out into jl-hdf5, jl-mpi packages etc.
    variant("cxx", default=False, description="Prepare for Julia Cxx package")
    variant("hdf5", default=False, description="Install Julia HDF5 package")
    variant("mpi", default=True, description="Install Julia MPI package")
    variant("plot", default=False,
            description="Install Julia plotting packages")
    variant("python", default=False,
            description="Install Julia Python package")
    variant("simd", default=False, description="Install Julia SIMD package")
    variant("mkl", default=False, description="Use Intel MKL")

    patch('gc.patch', when='@0.4:0.4.5')
    patch('openblas.patch', when='@0.4:0.4.5')
    patch('armgcc.patch', when='@1.0.0:1.1.1 %gcc@:5.9 target=aarch64:')

    variant('binutils', default=sys.platform != 'darwin',
            description="Build via binutils")

    # Build-time dependencies:
    # depends_on("awk")
    depends_on("m4", type="build")
    # depends_on("pkgconfig")

    # Combined build-time and run-time dependencies:
    # (Yes, these are run-time dependencies used by Julia's package manager.)
    depends_on("binutils", when='+binutils')
    depends_on("cmake @2.8:")
    depends_on("curl")
    depends_on("git", when='@:0.4')
    depends_on("git", when='@release-0.4')
    depends_on("openssl")
    depends_on("python@2.7:2.8")
    depends_on("mkl", when='+mkl')

    # Run-time dependencies:
    # depends_on("arpack")
    # depends_on("fftw +float")
    # depends_on("gmp")
    # depends_on("libgit")
    # depends_on("mpfr")
    # depends_on("openblas")
    # depends_on("pcre2")

    # ARPACK: Requires BLAS and LAPACK; needs to use the same version
    # as Julia.

    # BLAS and LAPACK: Julia prefers 64-bit versions on 64-bit
    # systems. OpenBLAS has an option for this; make it available as
    # variant.

    # FFTW: Something doesn't work when using a pre-installed FFTW
    # library; need to investigate.

    # GMP, MPFR: Something doesn't work when using a pre-installed
    # FFTW library; need to investigate.

    # LLVM: Julia works only with specific versions, and might require
    # patches. Thus we let Julia install its own LLVM.

    # Other possible dependencies:
    # USE_SYSTEM_OPENLIBM=0
    # USE_SYSTEM_OPENSPECFUN=0
    # USE_SYSTEM_DSFMT=0
    # USE_SYSTEM_SUITESPARSE=0
    # USE_SYSTEM_UTF8PROC=0
    # USE_SYSTEM_LIBGIT2=0

    # Run-time dependencies for Julia packages:
    depends_on("hdf5", when="+hdf5", type="run")
    depends_on("mpi", when="+mpi", type="run")
    depends_on("py-matplotlib", when="+plot", type="run")

    conflicts("@:0.7.0", when="target=aarch64:")

    def install(self, spec, prefix):
        # Julia needs git tags
        if os.path.isfile(".git/shallow"):
            git = which("git")
            git("fetch", "--unshallow")
        # Explicitly setting CC, CXX, or FC breaks building libuv, one
        # of Julia's dependencies. This might be a Darwin-specific
        # problem. Given how Spack sets up compilers, Julia should
        # still use Spack's compilers, even if we don't specify them
        # explicitly.
        options = [
            # "CC=cc",
            # "CXX=c++",
            # "FC=fc",
            # "USE_SYSTEM_ARPACK=1",
            "override USE_SYSTEM_CURL=1",
            # "USE_SYSTEM_FFTW=1",
            # "USE_SYSTEM_GMP=1",
            # "USE_SYSTEM_MPFR=1",
            # "USE_SYSTEM_PCRE=1",
            "prefix=%s" % prefix]
        if "+cxx" in spec:
            if "@master" not in spec:
                raise InstallError(
                    "Variant +cxx requires the @master version of Julia")
            options += [
                "BUILD_LLVM_CLANG=1",
                "LLVM_ASSERTIONS=1",
                "USE_LLVM_SHLIB=1"]
        if spec.target.family == 'aarch64':
            options += [
                'JULIA_CPU_TARGET=generic',
                'MARCH=armv8-a+crc']
        if '+mkl' in spec:
            options += [
                'USE_INTEL_MKL=1']
        with open('Make.user', 'w') as f:
            f.write('\n'.join(options) + '\n')
        make()
        make("install")

        # Julia's package manager needs a certificate
        cacert_dir = join_path(prefix, "etc", "curl")
        mkdirp(cacert_dir)
        cacert_file = join_path(cacert_dir, "cacert.pem")
        curl = which("curl")
        curl("--create-dirs",
             "--output", cacert_file,
             "https://curl.haxx.se/ca/cacert.pem")

        # Put Julia's compiler cache into a private directory
        cachedir = join_path(prefix, "var", "julia", "cache")
        mkdirp(cachedir)

        # Store Julia packages in a private directory
        pkgdir = join_path(prefix, "var", "julia", "pkg")
        mkdirp(pkgdir)

        # Configure Julia
        if spec.satisfies('@master') or spec.satisfies("@0.7:"):
            julia_config = 'startup.jl'
            cache_path = 'DEPOT_PATH'
            unshift = 'pushfirst!'
        else:
            julia_config = 'juliarc.jl'
            cache_path = 'LOAD_CACHE_PATH'
            unshift = 'unshift!'
        with open(join_path(prefix, "etc", "julia", julia_config),
                  "a") as juliarc:
            if "@master" in spec or "@release-0.5" in spec or "@0.5" in spec:
                # This is required for versions @0.5:
                juliarc.write(
                    '# Point package manager to working certificates\n')
                if spec.satisfies('@master') or spec.satisfies('@0,7'):
                    juliarc.write('import LibGit2;')
                juliarc.write('LibGit2.set_ssl_cert_locations("%s")\n' %
                              cacert_file)
                juliarc.write('\n')
            juliarc.write('# Put compiler cache into a private directory\n')
            juliarc.write('empty!(Base.%s)\n' % cache_path)
            juliarc.write('%s(Base.%s, "%s")\n' %
                          (unshift, cache_path, cachedir))
            juliarc.write('\n')
            juliarc.write('# Put Julia packages into a private directory\n')
            juliarc.write('ENV["JULIA_PKGDIR"] = "%s"\n' % pkgdir)
            juliarc.write('\n')

        # Install some commonly used packages
        julia = spec['julia'].command
        if spec.satisfies("@:0.7"):
            julia("-e", 'Pkg.init(); Pkg.update()')
            pkgstart = ''
        else:
            pkgstart = 'import Pkg;'

        # Install HDF5
        if "+hdf5" in spec:
            with open(join_path(prefix, "etc", "julia", julia_config),
                      "a") as juliarc:
                juliarc.write('# HDF5\n')
                juliarc.write('push!(Libdl.DL_LOAD_PATH, "%s")\n' %
                              spec["hdf5"].prefix.lib)
                juliarc.write('\n')
            julia("-e", pkgstart + 'Pkg.add("HDF5"); using HDF5')
            julia("-e", pkgstart + 'Pkg.add("JLD"); using JLD')

        # Install MPI
        if "+mpi" in spec:
            with open(join_path(prefix, "etc", "julia", julia_config),
                      "a") as juliarc:
                juliarc.write('# MPI\n')
                juliarc.write('ENV["JULIA_MPI_C_COMPILER"] = "%s"\n' %
                              join_path(spec["mpi"].prefix.bin, "mpicc"))
                juliarc.write('ENV["JULIA_MPI_Fortran_COMPILER"] = "%s"\n' %
                              join_path(spec["mpi"].prefix.bin, "mpifort"))
                juliarc.write('\n')
            julia("-e", pkgstart + 'Pkg.add("MPI"); using MPI')

        # Install Python
        if "+python" in spec or "+plot" in spec:
            with open(join_path(prefix, "etc", "julia", julia_config),
                      "a") as juliarc:
                juliarc.write('# Python\n')
                juliarc.write('ENV["PYTHON"] = "%s"\n' % spec["python"].home)
                juliarc.write('\n')
            # Python's OpenSSL package installer complains:
            # Error: PREFIX too long: 166 characters, but only 128 allowed
            # Error: post-link failed for: openssl-1.0.2g-0
            julia("-e", pkgstart + 'Pkg.add("PyCall"); using PyCall')

        if "+plot" in spec:
            julia("-e", pkgstart + 'Pkg.add("PyPlot"); using PyPlot')
            julia("-e", pkgstart + 'Pkg.add("Colors"); using Colors')
            # These require maybe gtk and imagemagick
            julia("-e", pkgstart + 'Pkg.add("Plots"); using Plots')
            julia("-e", pkgstart + 'Pkg.add("PlotRecipes"); using PlotRecipes')
            julia(
                "-e",
                pkgstart + 'Pkg.add("UnicodePlots"); using UnicodePlots'
            )
            julia("-e", """\
using Plots
using UnicodePlots
unicodeplots()
plot(x->sin(x)*cos(x), linspace(0, 2pi))
""")

        # Install SIMD
        if "+simd" in spec:
            julia("-e", pkgstart + 'Pkg.add("SIMD"); using SIMD')

        julia("-e", pkgstart + 'Pkg.status()')
