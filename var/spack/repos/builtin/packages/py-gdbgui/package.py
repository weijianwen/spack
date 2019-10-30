# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGdbgui(PythonPackage):
    """gdbgui is a modern, free, browser-based frontend to gdb"""

    homepage = "https://gdbgui.com"
    url      = "https://pypi.io/packages/source/g/gdbgui/gdbgui-0.11.2.1.tar.gz"

    version('0.11.2.1', sha256='280945a37414c31a798f68f70c1bffbedd12dfb0ce77418357e7d42b667491c7')

    depends_on('py-setuptools',             type=('build', 'run'))
    depends_on('py-flask@0.12.2:',          type=('build', 'run'))
    depends_on('py-flask-compress@1.4.0:',  type=('build', 'run'))
    depends_on('py-flask-socketio@2.9.3:',  type=('build', 'run'))
    depends_on('py-gevent@1.2.2:',          type=('build', 'run'))
    depends_on('py-pygdbmi@0.8.2.0:',       type=('build', 'run'))
    depends_on('py-pygments@2.2.0:',        type=('build', 'run'))
    depends_on('gdb',                       type='run')
