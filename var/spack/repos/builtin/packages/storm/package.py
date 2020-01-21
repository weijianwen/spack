# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Storm(Package):
    """
    Storm is a distributed realtime computation system. Similar to how
    Hadoop provides a set of general primitives for doing batch processing,
    Storm provides a set of general primitives for doing realtime computation.
    """

    homepage   = "https://www-eu.apache.org/dist/storm"
    url        = "https://www-eu.apache.org/dist/storm/apache-storm-2.1.0/apache-storm-2.1.0.tar.gz"
    url_list   = homepage
    list_depth = 2

    version('2.1.0', sha256='e279a495dda42af7d9051543989f74a1435a5bda53e795a1de4a1def32027fc4')
    version('2.0.0', sha256='0a4a6f985242a99f899a01bd01dacf9365f381e2acc473caa84073fbe84f6703')
    version('1.2.3', sha256='d45322253db06353a521284f31b30bd964dab859f3a279a305bd79112803425a')

    depends_on('java', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
