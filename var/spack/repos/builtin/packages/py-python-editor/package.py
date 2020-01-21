# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonEditor(PythonPackage):
    """python-editor is a library that provides the editor module for
    programmatically interfacing with your system's EDITOR variable."""

    homepage = "https://pypi.org/project/python-editor/"
    url      = "https://pypi.io/packages/source/p/python-editor/python-editor-1.0.4.tar.gz"

    version('1.0.4', sha256='51fda6bcc5ddbbb7063b2af7509e43bd84bfc32a4ff71349ec7847713882327b')

    depends_on('python@2.7:2.7.999,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
