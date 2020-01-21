# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

import pytest

import spack.main
import spack.binary_distribution

buildcache = spack.main.SpackCommand('buildcache')


@pytest.fixture()
def mock_get_specs(database, monkeypatch):
    specs = database.query_local()
    monkeypatch.setattr(
        spack.binary_distribution, 'get_specs', lambda x: specs
    )


@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
@pytest.mark.db
def test_buildcache_preview_just_runs(database):
    buildcache('preview', 'mpileaks')


@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
@pytest.mark.db
@pytest.mark.regression('13757')
def test_buildcache_list_duplicates(mock_get_specs, capsys):
    with capsys.disabled():
        output = buildcache('list', 'mpileaks', '@2.3')

    assert output.count('mpileaks') == 3
