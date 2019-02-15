# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import PackageBase
from spack.directives import depends_on, variant, conflicts

import spack.variant


class CudaPackage(PackageBase):
    """Auxiliary class which contains CUDA variant, dependencies and conflicts
    and is meant to unify and facilitate its usage.
    """

    # FIXME: keep cuda and cuda_arch separate to make usage easier untill
    # Spack has depends_on(cuda, when='cuda_arch!=None') or alike
    variant('cuda', default=False,
            description='Build with CUDA')
    # see http://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#gpu-feature-list
    # https://developer.nvidia.com/cuda-gpus
    variant('cuda_arch',
            description='CUDA architecture',
            values=spack.variant.any_combination_of(
                '20', '30', '32', '35', '50', '52', '53', '60', '61',
                '62', '70', '72', '75'
            ))

    # see http://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#nvcc-examples
    # and http://llvm.org/docs/CompileCudaWithLLVM.html#compiling-cuda-code
    @staticmethod
    def cuda_flags(arch_list):
        return [('--generate-code arch=compute_{0},code=sm_{0} '
                 '--generate-code arch=compute_{0},code=compute_{0}').format(s)
                for s in arch_list]

    depends_on("cuda@7:", when='+cuda')

    # CUDA version vs Architecture
    depends_on("cuda@8:", when='cuda_arch=60')
    depends_on("cuda@8:", when='cuda_arch=61')
    depends_on("cuda@8:", when='cuda_arch=62')
    depends_on("cuda@9:", when='cuda_arch=70')
    depends_on("cuda@9:", when='cuda_arch=72')
    depends_on("cuda@10:", when='cuda_arch=75')

    depends_on('cuda@:8', when='cuda_arch=20')

    # There are at least three cases to be aware of for compiler conflicts
    # 1. Linux x86_64
    # 2. Linux ppc64le
    # 3. Mac OS X

    # Linux x86_64 compiler conflicts from here:
    # https://gist.github.com/ax3l/9489132
    arch_platform = ' arch=x86_64 platform=linux'
    conflicts('%gcc@5:', when='+cuda ^cuda@:7.5' + arch_platform)
    conflicts('%gcc@6:', when='+cuda ^cuda@:8' + arch_platform)
    conflicts('%gcc@7:', when='+cuda ^cuda@:9.1' + arch_platform)
    conflicts('%gcc@8:', when='+cuda ^cuda@10.0.130' + arch_platform)
    conflicts('%pgi@:14.8', when='+cuda ^cuda@:7.0.27' + arch_platform)
    conflicts('%pgi@:15.3,15.5:', when='+cuda ^cuda@7.5' + arch_platform)
    conflicts('%pgi@:16.2,16.0:16.3', when='+cuda ^cuda@8' + arch_platform)
    conflicts('%pgi@:15,18:', when='+cuda ^cuda@9.0:9.1' + arch_platform)
    conflicts('%pgi@:16', when='+cuda ^cuda@9.2.88:10' + arch_platform)
    conflicts('%clang@:3.4', when='+cuda ^cuda@:7.5' + arch_platform)
    conflicts('%clang@:3.7,4:',
              when='+cuda ^cuda@8.0:9.0' + arch_platform)
    conflicts('%clang@:3.7,4.1:',
              when='+cuda ^cuda@9.1' + arch_platform)
    conflicts('%clang@:3.7,5.1:', when='+cuda ^cuda@9.2' + arch_platform)
    conflicts('%clang@:3.7,6.1:', when='+cuda ^cuda@10.0.130' + arch_platform)

    # x86_64 vs. ppc64le differ according to NVidia docs
    # Linux ppc64le compiler conflicts from Table from the docs below:
    # https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html
    # https://docs.nvidia.com/cuda/archive/9.2/cuda-installation-guide-linux/index.html
    # https://docs.nvidia.com/cuda/archive/9.1/cuda-installation-guide-linux/index.html
    # https://docs.nvidia.com/cuda/archive/9.0/cuda-installation-guide-linux/index.html
    # https://docs.nvidia.com/cuda/archive/8.0/cuda-installation-guide-linux/index.html

    arch_platform = ' arch=ppc64le platform=linux'
    # information prior to CUDA 9 difficult to find
    conflicts('%gcc@6:', when='+cuda ^cuda@:9' + arch_platform)
    conflicts('%gcc@8:', when='+cuda ^cuda@10.0.130' + arch_platform)
    conflicts('%pgi', when='+cuda ^cuda@:8' + arch_platform)
    conflicts('%pgi@:16', when='+cuda ^cuda@:9.1.185' + arch_platform)
    conflicts('%pgi@:17', when='+cuda ^cuda@:10' + arch_platform)
    conflicts('%clang@4:', when='+cuda ^cuda@:9.0.176' + arch_platform)
    conflicts('%clang@5:', when='+cuda ^cuda@:9.1' + arch_platform)
    conflicts('%clang@6:', when='+cuda ^cuda@:9.2' + arch_platform)
    conflicts('%clang@7:', when='+cuda ^cuda@10.0.130' + arch_platform)

    # Intel is mostly relevant for x86_64 Linux, even though it also
    # exists for Mac OS X.
    conflicts('%intel@:14,16:', when='+cuda ^cuda@7.5')
    conflicts('%intel@:14,17:', when='+cuda ^cuda@8.0.44')
    conflicts('%intel@:14,18:', when='+cuda ^cuda@8.0.61:9.1')
    conflicts('%intel@17:18', when='+cuda ^cuda@9.2:')
    conflicts('%intel@19:', when='+cuda')

    # XL is mostly relevant for ppc64le Linux
    conflicts('%xl@:12,14:', when='+cuda ^cuda@:9.1')
    conflicts('%xl@:12,14:15,17:', when='+cuda ^cuda@9.2')
    conflicts('%xl@17:', when='+cuda ^cuda@10.0.130')

    # Mac OS X
    # platform = ' platform=darwin'
    # Apple XCode clang vs. LLVM clang are difficult to specify
    # with spack syntax. Xcode clang name is `clang@x.y.z-apple`
    # which precludes ranges being specified. We have proposed
    # rename XCode clang to `clang@apple-x.y.z` or even
    # `clang-apple@x.y.z as a possible fix.
    # Compiler conflicts will be eventual taken from here:
    # https://docs.nvidia.com/cuda/cuda-installation-guide-mac-os-x/index.html#abstract

    # Make sure cuda_arch can not be used without +cuda
    conflicts('~cuda', when='cuda_arch=20')
    conflicts('~cuda', when='cuda_arch=30')
    conflicts('~cuda', when='cuda_arch=32')
    conflicts('~cuda', when='cuda_arch=35')
    conflicts('~cuda', when='cuda_arch=50')
    conflicts('~cuda', when='cuda_arch=52')
    conflicts('~cuda', when='cuda_arch=53')
    conflicts('~cuda', when='cuda_arch=60')
    conflicts('~cuda', when='cuda_arch=61')
    conflicts('~cuda', when='cuda_arch=62')
    conflicts('~cuda', when='cuda_arch=70')
    conflicts('~cuda', when='cuda_arch=72')
    conflicts('~cuda', when='cuda_arch=75')
