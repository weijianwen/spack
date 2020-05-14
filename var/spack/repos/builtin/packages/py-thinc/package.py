# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyThinc(PythonPackage):
    """Thinc: Practical Machine Learning for NLP in Python."""

    homepage = "https://github.com/explosion/thinc"
    url      = "https://pypi.io/packages/source/t/thinc/thinc-7.4.0.tar.gz"

    version('7.4.0', sha256='523e9be1bfaa3ed1d03d406ce451b6b4793a9719d5b83d2ea6b3398b96bc58b8')

    depends_on('py-setuptools', type='build')
    depends_on('py-murmurhash@0.28:1.0', type=('build', 'run'))
    depends_on('py-cymem@2.0.2:2.0.999', type=('build', 'run'))
    depends_on('py-preshed@1.0.1:3.0', type=('build', 'run'))
    depends_on('py-blis@0.4.0:0.4.999', type=('build', 'run'))
    depends_on('py-wasabi@0.0.9:1.0', type=('build', 'run'))
    depends_on('py-srsly@0.0.6:1.0', type=('build', 'run'))
    depends_on('py-catalogue@0.0.7:1.0', type=('build', 'run'))
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-plac@0.9.6:1.1', type=('build', 'run'))
    depends_on('py-tqdm@4.10:4.999', type=('build', 'run'))
    depends_on('py-pathlib@1.0.1', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-pytest', type='test')
    depends_on('py-mock', type='test')
    depends_on('py-hypothesis', type='test')
