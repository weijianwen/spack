# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCachedProperty(PythonPackage):
    """A decorator for caching properties in classes."""

    homepage = "https://pypi.org/project/cached-property/"
    url      = "https://pypi.io/packages/source/c/cached-property/cached-property-1.5.1.tar.gz"

    version('1.5.1', sha256="9217a59f14a5682da7c4b8829deadbfc194ac22e9908ccf7c8820234e80a1504")

    depends_on('py-setuptools', type='build')
