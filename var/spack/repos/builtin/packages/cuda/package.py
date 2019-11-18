# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from glob import glob
from llnl.util.filesystem import LibraryList
import os


class Cuda(Package):
    """CUDA is a parallel computing platform and programming model invented
    by NVIDIA. It enables dramatic increases in computing performance by
    harnessing the power of the graphics processing unit (GPU).

    Note: This package does not currently install the drivers necessary
    to run CUDA. These will need to be installed manually. See:
    https://docs.nvidia.com/cuda/ for details."""

    homepage = "https://developer.nvidia.com/cuda-zone"

    version('10.1.243',
            sha256='e7c22dc21278eb1b82f34a60ad7640b41ad3943d929bebda3008b72536855d31',
            expand=False,
            url="https://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.243_418.87.00_linux.run")
    version('10.0.130', sha256='92351f0e4346694d0fcb4ea1539856c9eb82060c25654463bfd8574ec35ee39a', expand=False,
            url="https://developer.nvidia.com/compute/cuda/10.0/Prod/local_installers/cuda_10.0.130_410.48_linux")
    version('9.2.88', sha256='8d02cc2a82f35b456d447df463148ac4cc823891be8820948109ad6186f2667c', expand=False,
            url="https://developer.nvidia.com/compute/cuda/9.2/Prod/local_installers/cuda_9.2.88_396.26_linux")
    version('9.1.85', sha256='8496c72b16fee61889f9281449b5d633d0b358b46579175c275d85c9205fe953', expand=False,
            url="https://developer.nvidia.com/compute/cuda/9.1/Prod/local_installers/cuda_9.1.85_387.26_linux")
    version('9.0.176', sha256='96863423feaa50b5c1c5e1b9ec537ef7ba77576a3986652351ae43e66bcd080c', expand=False,
            url="https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run")
    version('8.0.61', sha256='9ceca9c2397f841024e03410bfd6eabfd72b384256fbed1c1e4834b5b0ce9dc4', expand=False,
            url="https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda_8.0.61_375.26_linux-run")
    version('8.0.44', sha256='64dc4ab867261a0d690735c46d7cc9fc60d989da0d69dc04d1714e409cacbdf0', expand=False,
            url="https://developer.nvidia.com/compute/cuda/8.0/prod/local_installers/cuda_8.0.44_linux-run")
    version('7.5.18', sha256='08411d536741075131a1858a68615b8b73c51988e616e83b835e4632eea75eec', expand=False,
            url="http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda_7.5.18_linux.run")
    version('6.5.14', sha256='f3e527f34f317314fe8fcd8c85f10560729069298c0f73105ba89225db69da48', expand=False,
            url="http://developer.download.nvidia.com/compute/cuda/6_5/rel/installers/cuda_6.5.14_linux_64.run")

    # macOS Mojave drops NVIDIA graphics card support -- official NVIDIA
    # drivers do not exist for Mojave. See
    # https://devtalk.nvidia.com/default/topic/1043070/announcements/faq-about-macos-10-14-mojave-nvidia-drivers/
    # Note that a CUDA Toolkit installer does exist for macOS Mojave at
    # https://developer.nvidia.com/compute/cuda/10.1/Prod1/local_installers/cuda_10.1.168_mac.dmg,
    # but support for Mojave is dropped in later versions, and none of the
    # macOS NVIDIA drivers at
    # https://www.nvidia.com/en-us/drivers/cuda/mac-driver-archive/ mention
    # Mojave support -- only macOS High Sierra 10.13 is supported.
    conflicts('arch=darwin-mojave-x86_64')

    def setup_environment(self, spack_env, run_env):
        run_env.set('CUDA_HOME', self.prefix)

    def install(self, spec, prefix):
        runfile = glob(join_path(self.stage.source_path, 'cuda*_linux*'))[0]
        chmod = which('chmod')
        chmod('+x', runfile)
        runfile = which(runfile)

        # Note: NVIDIA does not officially support many newer versions of
        # compilers.  For example, on CentOS 6, you must use GCC 4.4.7 or
        # older. See:
        # http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#system-requirements
        # https://gist.github.com/ax3l/9489132
        # for details.

        # CUDA 10.1+ has different cmdline options for the installer
        arguments = [
            '--silent',         # disable interactive prompts
            '--override',       # override compiler version checks
            '--toolkit',        # install CUDA Toolkit
        ]
        if spec.satisfies('@10.1:'):
            arguments.append('--installpath=%s' % prefix)   # Where to install
        else:
            arguments.append('--verbose')                   # Verbose log file
            arguments.append('--toolkitpath=%s' % prefix)   # Where to install

        runfile(*arguments)

    @property
    def libs(self):
        libs = find_libraries('libcuda', root=self.prefix, shared=True,
                              recursive=True)

        filtered_libs = []
        # CUDA 10.0 provides Compatability libraries for running newer versions
        # of CUDA with older drivers. These do not work with newer drivers.
        for lib in libs:
            if 'compat' not in lib.split(os.sep):
                filtered_libs.append(lib)
        return LibraryList(filtered_libs)
