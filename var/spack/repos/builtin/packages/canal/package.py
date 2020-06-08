# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Canal(Package):
    """Alibaba MySQL binlog incremental subscription & consumer components."""

    homepage = "https://github.com/alibaba/canal/wiki"
    url      = "https://github.com/alibaba/canal/archive/canal-1.1.4.tar.gz"

    version('1.1.4', sha256='740e0adac56d7f281cba21eca173eef3e8d42aa3e0fb49709f92cb6a1451dfbc')
    version('1.1.3', sha256='3fe75ca5eb5cb97eb35818426c1427542ccddb0de052cf154e948ef321822cbc')
    version('1.1.2', sha256='097190f952bdf09b835ed68966f5a98fa8308322a6aab11c1bfd16cec1800cf2')

    depends_on('maven', type='build')
    depends_on('java', type=('build', 'run'))

    def install(self, spec, prefix):
        mvn = which('mvn')
        mvn('install', '-DskipTests')
        install_tree('.', prefix)
