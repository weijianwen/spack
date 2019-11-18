# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from os.path import split


class Miniconda3(Package):
    """The minimalist bootstrap toolset for conda and Python3."""

    homepage = "https://conda.io/miniconda.html"
    url      = "https://repo.continuum.io/miniconda/Miniconda3-4.6.14-Linux-x86_64.sh"

    version('4.6.14', sha256='0d6b23895a91294a4924bd685a3a1f48e35a17970a073cd2f684ffe2c31fc4be', expand=False)
    version('4.5.11', sha256='ea4594241e13a2671c5b158b3b813f0794fe58d514795fbf72a1aad24db918cf', expand=False)
    version('4.5.4', sha256='80ecc86f8c2f131c5170e43df489514f80e3971dd105c075935470bbf2476dea', expand=False)
    version('4.3.30', sha256='66c822dfe76636b4cc2ae5604816e0e723aa01620f50087f06410ecf5bfdf38c', expand=False)
    version('4.3.14', sha256='902f31a46b4a05477a9862485be5f84af761a444f8813345ff8dad8f6d3bccb2', expand=False)
    version('4.3.11', sha256='b9fe70ce7b6fa8df05abfb56995959b897d0365299f5046063bc236843474fb8', expand=False)

    def install(self, spec, prefix):
        # peel the name of the script out of the pathname of the
        # downloaded file
        dir, script = split(self.stage.archive_file)
        bash = which('bash')
        bash(script, '-b', '-f', '-p', self.prefix)
