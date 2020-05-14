# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class VotcaCsgapps(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the VOTCA coarse-graining extra apps.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/csgapps/tarball/v1.4"
    git      = "https://github.com/votca/csgapps.git"
    maintainers = ['junghans']

    version('master', branch='master')
    version('stable', branch='stable')
    version('1.6', sha256='084bbc5b179bb7eb8f6671d2d5fa13e69e68946570c9120a7e4b10aff1866e2e')
    version('1.5.1',   sha256='b4946711e88a1745688b6cce5aad872e6e2ea200fededf38d77a864883e3750e')
    version('1.5',     sha256='18b40ce6222509bc70aa9d56b8c538cd5903edf7294d6f95530668e555206d5b')
    version('1.4.1',   sha256='095d9ee4cd49d2fd79c10e0e84e6890b755e54dec6a5cd580a2b4241ba230a2b')
    version('1.4',     sha256='4ea8348c2f7de3cc488f48fbd8652e69b52515441952766c06ff67ed1aaf69a0')

    for v in ["1.4", "1.4.1", "1.5", "1.5.1", "1.6", "master", "stable"]:
        depends_on('votca-csg@%s' % v, when="@%s:%s.0" % (v, v))
    depends_on("boost")
