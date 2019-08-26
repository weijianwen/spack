# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPoster(PythonPackage):
    """Streaming HTTP uploads and multipart/form-data encoding."""

    homepage = "https://pypi.org/project/poster/"
    url      = "https://atlee.ca/software/poster/dist/0.8.1/poster-0.8.1.tar.gz"

    version('0.8.1', '2db12704538781fbaa7e63f1505d6fc8')

    depends_on('py-setuptools', type='build')

    # https://bitbucket.org/chrisatlee/poster/issues/24/not-working-with-python3
    # https://bitbucket.org/chrisatlee/poster/issues/25/poster-connot-work-in-python35
    # Patch created using 2to3
    patch('python3.patch', when='^python@3:')
