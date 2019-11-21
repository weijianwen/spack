# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Caches used by Spack to store data"""
import os

import llnl.util.lang
from llnl.util.filesystem import mkdirp

import spack.error
import spack.paths
import spack.config
import spack.fetch_strategy
import spack.util.file_cache
import spack.util.path


def _misc_cache():
    """The ``misc_cache`` is Spack's cache for small data.

    Currently the ``misc_cache`` stores indexes for virtual dependency
    providers and for which packages provide which tags.
    """
    path = spack.config.get('config:misc_cache')
    if not path:
        path = os.path.join(spack.paths.user_config_path, 'cache')
    path = spack.util.path.canonicalize_path(path)

    return spack.util.file_cache.FileCache(path)


#: Spack's cache for small data
misc_cache = llnl.util.lang.Singleton(_misc_cache)


def _fetch_cache():
    """Filesystem cache of downloaded archives.

    This prevents Spack from repeatedly fetch the same files when
    building the same package different ways or multiple times.
    """
    path = spack.config.get('config:source_cache')
    if not path:
        path = os.path.join(spack.paths.var_path, "cache")
    path = spack.util.path.canonicalize_path(path)

    return spack.fetch_strategy.FsCache(path)


class MirrorCache(object):
    def __init__(self, root):
        self.root = os.path.abspath(root)

    def store(self, fetcher, relative_dest):
        """Fetch and relocate the fetcher's target into our mirror cache."""

        # Note this will archive package sources even if they would not
        # normally be cached (e.g. the current tip of an hg/git branch)
        dst = os.path.join(self.root, relative_dest)
        mkdirp(os.path.dirname(dst))
        fetcher.archive(dst)

    def symlink(self, mirror_ref):
        """Symlink a human readible path in our mirror to the actual
        storage location."""

        cosmetic_path = os.path.join(self.root, mirror_ref.cosmetic_path)
        relative_dst = os.path.relpath(
            mirror_ref.storage_path,
            start=os.path.dirname(cosmetic_path))
        if not os.path.exists(cosmetic_path):
            mkdirp(os.path.dirname(cosmetic_path))
            os.symlink(relative_dst, cosmetic_path)


#: Spack's local cache for downloaded source archives
fetch_cache = llnl.util.lang.Singleton(_fetch_cache)

mirror_cache = None
