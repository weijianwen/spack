# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GitLfs(MakefilePackage):
    """Git LFS is a system for managing and versioning large files in
       association with a Git repository.  Instead of storing the large files
       within the Git repository as blobs, Git LFS stores special "pointer
       files" in the repository, while storing the actual file contents on a
       Git LFS server."""

    homepage = "https://git-lfs.github.com"
    url      = "https://github.com/git-lfs/git-lfs/archive/v2.6.1.tar.gz"

    version('2.7.1', sha256='af60c2370d135ab13724d302a0b1c226ec9fb0ee6d29ecc335e9add4c86497b4')
    version('2.7.0', sha256='1c829ddd163be2206a44edb366bd7f6d84c5afae3496687405ca9d2a5f3af07b')
    version('2.6.1', sha256='e17cd9d4e66d1116be32f7ddc7e660c7f8fabbf510bc01b01ec15a22dd934ead')

    depends_on('go@1.5:', type='build')
    depends_on('git@1.8.2:', type='run')

    patch('patches/issue-10702.patch', when='@2.7.0:2.7.1')

    parallel = False

    # Git-lfs does not provide an 'install' target in the Makefile
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path('bin', 'git-lfs'), prefix.bin)
