# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Chill(AutotoolsPackage):
    """A polyheadral compiler for autotuning"""

    homepage = "http://github.com/CtopCsUtahEdu/chill"
    url      = "https://github.com/CtopCsUtahEdu/chill/archive/v0.3.tar.gz"
    git      = "https://github.com/CtopCsUtahEdu/chill.git"

    maintainers = ['dhuth']

    version('master', branch='master')
    version('0.3', sha256='574b622368a6bfaadbe9c1fa02fabefdc6c006069246f67d299f943b7e1d8aa3')

    depends_on('boost@1.66.0 cxxstd=11', type='build')
    depends_on('rose@0.9.10.0 +cxx11', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake@1.14:',  type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('iegenlib', type='build')
    depends_on('bison@3.4', type='build')
    depends_on('flex', type='build')
    depends_on('python')

    build_directory = 'spack-build'

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./bootstrap')

    def setup_build_environment(self, env):
        rose_home  = self.spec['rose'].prefix
        boost_home = self.spec['boost'].prefix
        iegen_home = self.spec['iegenlib'].prefix

        env.set('ROSEHOME', rose_home)
        env.set('BOOSTHOME', boost_home)
        env.set('IEGENHOME', iegen_home)

        env.append_path('LD_LIBRARY_PATH', rose_home.lib)
        env.append_path('LD_LIBRARY_PATH', boost_home.lib)
        env.append_path('LD_LIBRARY_PATH', iegen_home.lib)

    def setup_run_environment(self, env):
        rose_home  = self.spec['rose'].prefix
        boost_home = self.spec['boost'].prefix
        iegen_home = self.spec['iegenlib'].prefix

        env.append_path('LD_LIBRARY_PATH', rose_home.lib)
        env.append_path('LD_LIBRARY_PATH', boost_home.lib)
        env.append_path('LD_LIBRARY_PATH', iegen_home.lib)

    def configure_args(self):
        args = ['--with-rose={0}'.format(self.spec['rose'].prefix),
                '--with-boost={0}'.format(self.spec['boost'].prefix),
                '--with-iegen={0}'.format(self.spec['iegenlib'].prefix)]

        return args
