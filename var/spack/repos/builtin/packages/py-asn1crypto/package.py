# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyAsn1crypto(PythonPackage):
    """Python ASN.1 library with a focus on performance and a pythonic API """

    homepage = "https://github.com/wbond/asn1crypto"
    url      = "https://pypi.io/packages/source/a/asn1crypto/asn1crypto-0.22.0.tar.gz"

    version('0.22.0', sha256='cbbadd640d3165ab24b06ef25d1dca09a3441611ac15f6a6b452474fdf0aed1a')

    depends_on('py-setuptools', type='build')
