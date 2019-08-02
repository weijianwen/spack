# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyOnnx(PythonPackage):
    """Open Neural Network Exchange (ONNX) is an open ecosystem that
       empowers AI developers to choose the right tools as their
       project evolves. ONNX provides an open source format for AI
       models, both deep learning and traditional ML. It defines an
       extensible computation graph model, as well as definitions of
       built-in operators and standard data types. Currently we focus
       on the capabilities needed for inferencing (scoring)."""

    homepage = "https://github.com/onnx/onnx"
    url      = "https://pypi.io/packages/source/O/Onnx/onnx-1.5.0.tar.gz"

    version('1.5.0', sha256='1a584a4ef62a6db178c257fffb06a9d8e61b41c0a80bfd8bcd8a253d72c4b0b4')

    depends_on('py-setuptools', type='build')
    depends_on('protobuf')
    depends_on('py-protobuf+cpp', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-typing@3.6.4:', type=('build', 'run'))
    depends_on('py-typing-extensions@3.6.4:', type=('build', 'run'))
