# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIpython(PythonPackage):
    """IPython provides a rich toolkit to help you make the most out of using
       Python interactively."""
    homepage = "https://pypi.python.org/pypi/ipython"
    url      = "https://pypi.io/packages/source/i/ipython/ipython-2.3.1.tar.gz"

    version('7.5.0', sha256='e840810029224b56cd0d9e7719dc3b39cf84d577f8ac686547c8ba7a06eeab26')
    version('7.3.0', sha256='06de667a9e406924f97781bda22d5d76bfb39762b678762d86a466e63f65dc39')
    version('5.8.0', sha256='4bac649857611baaaf76bc82c173aa542f7486446c335fe1a6c05d0d491c8906')
    version('5.1.0', sha256='7ef4694e1345913182126b219aaa4a0047e191af414256da6772cf249571b961')
    version('3.1.0', sha256='532092d3f06f82b1d8d1e5c37097eae19fcf025f8f6a4b670dd49c3c338d5624')
    version('2.3.1', sha256='3e98466aa2fe54540bcba9aa6e01a39f40110d67668c297340c4b9514b7cc49c')

    depends_on('python@3.6:', type=('build', 'run'), when='@7.10:')
    depends_on('python@3.5:', type=('build', 'run'), when='@7:')
    depends_on('python@3.3:', type=('build', 'run'), when='@6:')
    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))

    depends_on('py-backports-shutil-get-terminal-size', type=('build', 'run'), when="^python@:3.2")
    depends_on('py-pathlib2', type=('build', 'run'), when="^python@:3.3")
    depends_on('py-pygments',                   type=('build', 'run'))
    depends_on('py-pickleshare',                type=('build', 'run'))
    depends_on('py-simplegeneric@0.8:',         type=('build', 'run'), when='@:7.0.0')
    depends_on('py-prompt-toolkit@1.0.4:1.999',  when='@:7.0.0', type=('build', 'run'))
    depends_on('py-prompt-toolkit@2.0.0:2.999',  when='@7.0.0:', type=('build', 'run'))
    depends_on('py-prompt-toolkit@2.0.0:2.0.999', when='@7.5.0:', type=('build', 'run'))
    depends_on('py-traitlets@4.2:',             type=('build', 'run'))
    depends_on('py-decorator',                  type=('build', 'run'))
    depends_on('py-pexpect',                    type=('build', 'run'))
    depends_on('py-backcall',                   type=('build', 'run'), when="^python@3.3:")
    depends_on('py-appnope', type=('build', 'run'), when='platform=darwin')
    depends_on('py-jedi@0.10:', type=('build', 'run'), when='@7.5.0:')
    depends_on('py-backcall', type=('build', 'run'), when='@7.5.0:')
    depends_on('py-setuptools@18.5:', type='run', when='@4.1:')
