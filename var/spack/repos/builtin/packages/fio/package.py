# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Fio(AutotoolsPackage):
    """Flexible I/O Tester.

    Fio spawns a number of threads or processes doing a particular type of I/O
    action as specified by the user. fio takes a number of global parameters,
    each inherited by the thread unless otherwise parameters given to them
    overriding that setting is given.
    """

    homepage = "https://github.com/axboe/fio"
    url = "https://github.com/axboe/fio/archive/fio-2.19.tar.gz"

    version('3.16', sha256='c7731a9e831581bab7104da9ea60c9f44e594438dbe95dff26726ca0285e7b93')
    version('2.19', sha256='61fb03a18703269b781aaf195cb0d7931493bbb5bfcc8eb746d5d66d04ed77f7')

    variant('gui', default=False, description='Enable building of gtk gfio')
    variant('doc', default=False, description='Generate documentation')
    variant('libaio', default=False, description='Enable libaio engine')

    depends_on('gtkplus@2.18:', when='+gui')
    depends_on('cairo',         when='+gui')
    depends_on('libaio',        when='+libaio')

    depends_on('py-sphinx', type='build', when='+doc')

    conflicts('+libaio', when='platform=darwin',
              msg='libaio does not support Darwin')

    def configure_args(self):
        config_args = []

        if '+gui' in self.spec:
            config_args.append('--enable-gfio')

        return config_args

    @run_after('build')
    def build_docs(self):
        if '+doc' in self.spec:
            make('-C', 'doc', 'html')
            make('-C', 'doc', 'man')
