# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyarrow(PythonPackage):
    """A cross-language development platform for in-memory data.

    This package contains the Python bindings.
    """

    homepage = "http://arrow.apache.org"
    url      = "https://pypi.org/packages/source/p/pyarrow/pyarrow-0.9.0.tar.gz"

    version('0.12.1', sha256='10db6e486c918c3af999d0114a22d92770687e3a6607ea3f14e6748854824c2a')
    version('0.11.0', sha256='07a6fd71c5d7440f2c42383dd2c5daa12d7f0a012f1e88288ed08a247032aead')
    version('0.9.0', sha256='7db8ce2f0eff5a00d6da918ce9f9cfec265e13f8a119b4adb1595e5b19fd6242')

    variant('parquet', default=False, description="Build with Parquet support")

    depends_on('cmake@3.0.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')

    for v in ('@0.9.0', '@0.11.0', '@0.12.1'):
        depends_on('arrow+python' + v, when=v)
        depends_on('arrow+parquet+python' + v, when='+parquet' + v)

    phases = ['build_ext', 'install']

    def build_ext_args(self, spec, prefix):
        args = []
        if spec.satisfies('+parquet'):
            args.append('--with-parquet')
        return args
