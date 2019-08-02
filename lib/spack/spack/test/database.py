# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
These tests check the database is functioning properly,
both in memory and in its file
"""
import datetime
import functools
import multiprocessing
import os
import pytest
import json

from llnl.util.tty.colify import colify

import spack.repo
import spack.store
import spack.database
import spack.package
import spack.spec
from spack.test.conftest import MockPackage, MockPackageMultiRepo
from spack.util.executable import Executable


pytestmark = pytest.mark.db


@pytest.fixture()
def test_store(tmpdir):
    real_store = spack.store.store
    spack.store.store = spack.store.Store(str(tmpdir.join('test_store')))

    yield

    spack.store.store = real_store


@pytest.fixture()
def upstream_and_downstream_db(tmpdir_factory, gen_mock_layout):
    mock_db_root = str(tmpdir_factory.mktemp('mock_db_root'))
    upstream_db = spack.database.Database(mock_db_root)
    # Generate initial DB file to avoid reindex
    with open(upstream_db._index_path, 'w') as db_file:
        upstream_db._write_to_file(db_file)
    upstream_layout = gen_mock_layout('/a/')

    downstream_db_root = str(
        tmpdir_factory.mktemp('mock_downstream_db_root'))
    downstream_db = spack.database.Database(
        downstream_db_root, upstream_dbs=[upstream_db])
    with open(downstream_db._index_path, 'w') as db_file:
        downstream_db._write_to_file(db_file)
    downstream_layout = gen_mock_layout('/b/')

    yield upstream_db, upstream_layout, downstream_db, downstream_layout


@pytest.mark.usefixtures('config')
def test_installed_upstream(upstream_and_downstream_db):
    upstream_db, upstream_layout, downstream_db, downstream_layout = (
        upstream_and_downstream_db)

    default = ('build', 'link')
    x = MockPackage('x', [], [])
    z = MockPackage('z', [], [])
    y = MockPackage('y', [z], [default])
    w = MockPackage('w', [x, y], [default, default])
    mock_repo = MockPackageMultiRepo([w, x, y, z])

    with spack.repo.swap(mock_repo):
        spec = spack.spec.Spec('w')
        spec.concretize()

        for dep in spec.traverse(root=False):
            upstream_db.add(dep, upstream_layout)

        new_spec = spack.spec.Spec('w')
        new_spec.concretize()
        downstream_db.add(new_spec, downstream_layout)
        for dep in new_spec.traverse(root=False):
            upstream, record = downstream_db.query_by_spec_hash(
                dep.dag_hash())
            assert upstream
            assert record.path == upstream_layout.path_for_spec(dep)
        upstream, record = downstream_db.query_by_spec_hash(
            new_spec.dag_hash())
        assert not upstream
        assert record.installed

        upstream_db._check_ref_counts()
        downstream_db._check_ref_counts()


@pytest.mark.usefixtures('config')
def test_removed_upstream_dep(upstream_and_downstream_db):
    upstream_db, upstream_layout, downstream_db, downstream_layout = (
        upstream_and_downstream_db)

    default = ('build', 'link')
    z = MockPackage('z', [], [])
    y = MockPackage('y', [z], [default])
    mock_repo = MockPackageMultiRepo([y, z])

    with spack.repo.swap(mock_repo):
        spec = spack.spec.Spec('y')
        spec.concretize()

        upstream_db.add(spec['z'], upstream_layout)

        new_spec = spack.spec.Spec('y')
        new_spec.concretize()
        downstream_db.add(new_spec, downstream_layout)

        upstream_db.remove(new_spec['z'])

        new_downstream = spack.database.Database(
            downstream_db.root, upstream_dbs=[upstream_db])
        new_downstream._fail_when_missing_deps = True
        with pytest.raises(spack.database.MissingDependenciesError):
            new_downstream._read()


@pytest.mark.usefixtures('config')
def test_add_to_upstream_after_downstream(upstream_and_downstream_db):
    """An upstream DB can add a package after it is installed in the downstream
    DB. When a package is recorded as installed in both, the results should
    refer to the downstream DB.
    """
    upstream_db, upstream_layout, downstream_db, downstream_layout = (
        upstream_and_downstream_db)

    x = MockPackage('x', [], [])
    mock_repo = MockPackageMultiRepo([x])

    with spack.repo.swap(mock_repo):
        spec = spack.spec.Spec('x')
        spec.concretize()

        downstream_db.add(spec, downstream_layout)

        upstream_db.add(spec, upstream_layout)

        upstream, record = downstream_db.query_by_spec_hash(spec.dag_hash())
        # Even though the package is recorded as installed in the upstream DB,
        # we prefer the locally-installed instance
        assert not upstream

        qresults = downstream_db.query('x')
        assert len(qresults) == 1
        queried_spec, = qresults
        try:
            orig_db = spack.store.db
            spack.store.db = downstream_db
            assert queried_spec.prefix == downstream_layout.path_for_spec(spec)
        finally:
            spack.store.db = orig_db


@pytest.mark.usefixtures('config')
def test_recursive_upstream_dbs(tmpdir_factory, test_store, gen_mock_layout):
    roots = [str(tmpdir_factory.mktemp(x)) for x in ['a', 'b', 'c']]
    layouts = [gen_mock_layout(x) for x in ['/ra/', '/rb/', '/rc/']]

    default = ('build', 'link')
    z = MockPackage('z', [], [])
    y = MockPackage('y', [z], [default])
    x = MockPackage('x', [y], [default])

    mock_repo = MockPackageMultiRepo([x, y, z])

    with spack.repo.swap(mock_repo):
        spec = spack.spec.Spec('x')
        spec.concretize()
        db_c = spack.database.Database(roots[2])
        db_c.add(spec['z'], layouts[2])

        db_b = spack.database.Database(roots[1], upstream_dbs=[db_c])
        db_b.add(spec['y'], layouts[1])

        db_a = spack.database.Database(roots[0], upstream_dbs=[db_b, db_c])
        db_a.add(spec['x'], layouts[0])

        dbs = spack.store._construct_upstream_dbs_from_install_roots(
            roots, _test=True)

        assert dbs[0].db_for_spec_hash(spec.dag_hash()) == dbs[0]
        assert dbs[0].db_for_spec_hash(spec['y'].dag_hash()) == dbs[1]
        assert dbs[0].db_for_spec_hash(spec['z'].dag_hash()) == dbs[2]

        dbs[0]._check_ref_counts()
        dbs[1]._check_ref_counts()
        dbs[2]._check_ref_counts()

        assert (dbs[0].installed_relatives(spec) ==
                set(spec.traverse(root=False)))
        assert (dbs[0].installed_relatives(spec['z'], direction='parents') ==
                set([spec, spec['y']]))
        assert not dbs[2].installed_relatives(spec['z'], direction='parents')


@pytest.fixture()
def usr_folder_exists(monkeypatch):
    """The ``/usr`` folder is assumed to be existing in some tests. This
    fixture makes it such that its existence is mocked, so we have no
    requirements on the system running tests.
    """
    isdir = os.path.isdir

    @functools.wraps(os.path.isdir)
    def mock_isdir(path):
        if path == '/usr':
            return True
        return isdir(path)

    monkeypatch.setattr(os.path, 'isdir', mock_isdir)


def _print_ref_counts():
    """Print out all ref counts for the graph used here, for debugging"""
    recs = []

    def add_rec(spec):
        cspecs = spack.store.db.query(spec, installed=any)

        if not cspecs:
            recs.append("[ %-7s ] %-20s-" % ('', spec))
        else:
            key = cspecs[0].dag_hash()
            rec = spack.store.db.get_record(cspecs[0])
            recs.append("[ %-7s ] %-20s%d" % (key[:7], spec, rec.ref_count))

    with spack.store.db.read_transaction():
        add_rec('mpileaks ^mpich')
        add_rec('callpath ^mpich')
        add_rec('mpich')

        add_rec('mpileaks ^mpich2')
        add_rec('callpath ^mpich2')
        add_rec('mpich2')

        add_rec('mpileaks ^zmpi')
        add_rec('callpath ^zmpi')
        add_rec('zmpi')
        add_rec('fake')

        add_rec('dyninst')
        add_rec('libdwarf')
        add_rec('libelf')

    colify(recs, cols=3)


def _check_merkleiness():
    """Ensure the spack database is a valid merkle graph."""
    all_specs = spack.store.db.query(installed=any)

    seen = {}
    for spec in all_specs:
        for dep in spec.dependencies():
            hash_key = dep.dag_hash()
            if hash_key not in seen:
                seen[hash_key] = id(dep)
            else:
                assert seen[hash_key] == id(dep)


def _check_db_sanity(database):
    """Utiilty function to check db against install layout."""
    pkg_in_layout = sorted(spack.store.layout.all_specs())
    actual = sorted(database.query())

    externals = sorted([x for x in actual if x.external])
    nexpected = len(pkg_in_layout) + len(externals)

    assert nexpected == len(actual)

    non_external_in_db = sorted([x for x in actual if not x.external])

    for e, a in zip(pkg_in_layout, non_external_in_db):
        assert e == a

    _check_merkleiness()


def _check_remove_and_add_package(database, spec):
    """Remove a spec from the DB, then add it and make sure everything's
    still ok once it is added.  This checks that it was
    removed, that it's back when added again, and that ref
    counts are consistent.
    """
    original = database.query()
    database._check_ref_counts()

    # Remove spec
    concrete_spec = database.remove(spec)
    database._check_ref_counts()
    remaining = database.query()

    # ensure spec we removed is gone
    assert len(original) - 1 == len(remaining)
    assert all(s in original for s in remaining)
    assert concrete_spec not in remaining

    # add it back and make sure everything is ok.
    database.add(concrete_spec, spack.store.layout)
    installed = database.query()
    assert concrete_spec in installed
    assert installed == original

    # sanity check against direcory layout and check ref counts.
    _check_db_sanity(database)
    database._check_ref_counts()


def _mock_install(spec):
    s = spack.spec.Spec(spec)
    s.concretize()
    pkg = spack.repo.get(s)
    pkg.do_install(fake=True)


def _mock_remove(spec):
    specs = spack.store.db.query(spec)
    assert len(specs) == 1
    spec = specs[0]
    spec.package.do_uninstall(spec)


def test_default_queries(database):
    # Testing a package whose name *doesn't* start with 'lib'
    # to ensure the library has 'lib' prepended to the name
    rec = database.get_record('zmpi')

    spec = rec.spec

    libraries = spec['zmpi'].libs
    assert len(libraries) == 1
    assert libraries.names[0] == 'zmpi'

    headers = spec['zmpi'].headers
    assert len(headers) == 1
    assert headers.names[0] == 'zmpi'

    command = spec['zmpi'].command
    assert isinstance(command, Executable)
    assert command.name == 'zmpi'
    assert os.path.exists(command.path)

    # Testing a package whose name *does* start with 'lib'
    # to ensure the library doesn't have a double 'lib' prefix
    rec = database.get_record('libelf')

    spec = rec.spec

    libraries = spec['libelf'].libs
    assert len(libraries) == 1
    assert libraries.names[0] == 'elf'

    headers = spec['libelf'].headers
    assert len(headers) == 1
    assert headers.names[0] == 'libelf'

    command = spec['libelf'].command
    assert isinstance(command, Executable)
    assert command.name == 'libelf'
    assert os.path.exists(command.path)


def test_005_db_exists(database):
    """Make sure db cache file exists after creating."""
    index_file = os.path.join(database.root, '.spack-db', 'index.json')
    lock_file = os.path.join(database.root, '.spack-db', 'lock')
    assert os.path.exists(str(index_file))
    assert os.path.exists(str(lock_file))


def test_010_all_install_sanity(database):
    """Ensure that the install layout reflects what we think it does."""
    all_specs = spack.store.layout.all_specs()
    assert len(all_specs) == 14

    # Query specs with multiple configurations
    mpileaks_specs = [s for s in all_specs if s.satisfies('mpileaks')]
    callpath_specs = [s for s in all_specs if s.satisfies('callpath')]
    mpi_specs = [s for s in all_specs if s.satisfies('mpi')]

    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 3
    assert len(mpi_specs) == 3

    # Query specs with single configurations
    dyninst_specs = [s for s in all_specs if s.satisfies('dyninst')]
    libdwarf_specs = [s for s in all_specs if s.satisfies('libdwarf')]
    libelf_specs = [s for s in all_specs if s.satisfies('libelf')]

    assert len(dyninst_specs) == 1
    assert len(libdwarf_specs) == 1
    assert len(libelf_specs) == 1

    # Query by dependency
    assert len(
        [s for s in all_specs if s.satisfies('mpileaks ^mpich')]
    ) == 1
    assert len(
        [s for s in all_specs if s.satisfies('mpileaks ^mpich2')]
    ) == 1
    assert len(
        [s for s in all_specs if s.satisfies('mpileaks ^zmpi')]
    ) == 1


def test_015_write_and_read(mutable_database):
    # write and read DB
    with spack.store.db.write_transaction():
        specs = spack.store.db.query()
        recs = [spack.store.db.get_record(s) for s in specs]

    for spec, rec in zip(specs, recs):
        new_rec = spack.store.db.get_record(spec)
        assert new_rec.ref_count == rec.ref_count
        assert new_rec.spec == rec.spec
        assert new_rec.path == rec.path
        assert new_rec.installed == rec.installed


def test_020_db_sanity(database):
    """Make sure query() returns what's actually in the db."""
    _check_db_sanity(database)


def test_025_reindex(mutable_database):
    """Make sure reindex works and ref counts are valid."""
    spack.store.store.reindex()
    _check_db_sanity(mutable_database)


def test_030_db_sanity_from_another_process(mutable_database):
    def read_and_modify():
        # check that other process can read DB
        _check_db_sanity(mutable_database)
        with mutable_database.write_transaction():
            _mock_remove('mpileaks ^zmpi')

    p = multiprocessing.Process(target=read_and_modify, args=())
    p.start()
    p.join()

    # ensure child process change is visible in parent process
    with mutable_database.read_transaction():
        assert len(mutable_database.query('mpileaks ^zmpi')) == 0


def test_040_ref_counts(database):
    """Ensure that we got ref counts right when we read the DB."""
    database._check_ref_counts()


def test_050_basic_query(database):
    """Ensure querying database is consistent with what is installed."""
    # query everything
    assert len(spack.store.db.query()) == 16

    # query specs with multiple configurations
    mpileaks_specs = database.query('mpileaks')
    callpath_specs = database.query('callpath')
    mpi_specs = database.query('mpi')

    assert len(mpileaks_specs) == 3
    assert len(callpath_specs) == 3
    assert len(mpi_specs) == 3

    # query specs with single configurations
    dyninst_specs = database.query('dyninst')
    libdwarf_specs = database.query('libdwarf')
    libelf_specs = database.query('libelf')

    assert len(dyninst_specs) == 1
    assert len(libdwarf_specs) == 1
    assert len(libelf_specs) == 1

    # Query by dependency
    assert len(database.query('mpileaks ^mpich')) == 1
    assert len(database.query('mpileaks ^mpich2')) == 1
    assert len(database.query('mpileaks ^zmpi')) == 1

    # Query by date
    assert len(database.query(start_date=datetime.datetime.min)) == 16
    assert len(database.query(start_date=datetime.datetime.max)) == 0
    assert len(database.query(end_date=datetime.datetime.min)) == 0
    assert len(database.query(end_date=datetime.datetime.max)) == 16


def test_060_remove_and_add_root_package(mutable_database):
    _check_remove_and_add_package(mutable_database, 'mpileaks ^mpich')


def test_070_remove_and_add_dependency_package(mutable_database):
    _check_remove_and_add_package(mutable_database, 'dyninst')


def test_080_root_ref_counts(mutable_database):
    rec = mutable_database.get_record('mpileaks ^mpich')

    # Remove a top-level spec from the DB
    mutable_database.remove('mpileaks ^mpich')

    # record no longer in DB
    assert mutable_database.query('mpileaks ^mpich', installed=any) == []

    # record's deps have updated ref_counts
    assert mutable_database.get_record('callpath ^mpich').ref_count == 0
    assert mutable_database.get_record('mpich').ref_count == 1

    # Put the spec back
    mutable_database.add(rec.spec, spack.store.layout)

    # record is present again
    assert len(mutable_database.query('mpileaks ^mpich', installed=any)) == 1

    # dependencies have ref counts updated
    assert mutable_database.get_record('callpath ^mpich').ref_count == 1
    assert mutable_database.get_record('mpich').ref_count == 2


def test_090_non_root_ref_counts(mutable_database):
    mutable_database.get_record('mpileaks ^mpich')
    mutable_database.get_record('callpath ^mpich')

    # "force remove" a non-root spec from the DB
    mutable_database.remove('callpath ^mpich')

    # record still in DB but marked uninstalled
    assert mutable_database.query('callpath ^mpich', installed=True) == []
    assert len(mutable_database.query('callpath ^mpich', installed=any)) == 1

    # record and its deps have same ref_counts
    assert mutable_database.get_record(
        'callpath ^mpich', installed=any
    ).ref_count == 1
    assert mutable_database.get_record('mpich').ref_count == 2

    # remove only dependent of uninstalled callpath record
    mutable_database.remove('mpileaks ^mpich')

    # record and parent are completely gone.
    assert mutable_database.query('mpileaks ^mpich', installed=any) == []
    assert mutable_database.query('callpath ^mpich', installed=any) == []

    # mpich ref count updated properly.
    mpich_rec = mutable_database.get_record('mpich')
    assert mpich_rec.ref_count == 0


def test_100_no_write_with_exception_on_remove(database):
    def fail_while_writing():
        with database.write_transaction():
            _mock_remove('mpileaks ^zmpi')
            raise Exception()

    with database.read_transaction():
        assert len(database.query('mpileaks ^zmpi', installed=any)) == 1

    with pytest.raises(Exception):
        fail_while_writing()

    # reload DB and make sure zmpi is still there.
    with database.read_transaction():
        assert len(database.query('mpileaks ^zmpi', installed=any)) == 1


def test_110_no_write_with_exception_on_install(database):
    def fail_while_writing():
        with database.write_transaction():
            _mock_install('cmake')
            raise Exception()

    with database.read_transaction():
        assert database.query('cmake', installed=any) == []

    with pytest.raises(Exception):
        fail_while_writing()

    # reload DB and make sure cmake was not written.
    with database.read_transaction():
        assert database.query('cmake', installed=any) == []


def test_115_reindex_with_packages_not_in_repo(mutable_database):
    # Dont add any package definitions to this repository, the idea is that
    # packages should not have to be defined in the repository once they
    # are installed
    with spack.repo.swap(MockPackageMultiRepo([])):
        spack.store.store.reindex()
        _check_db_sanity(mutable_database)


def test_external_entries_in_db(mutable_database):
    rec = mutable_database.get_record('mpileaks ^zmpi')
    assert rec.spec.external_path is None
    assert rec.spec.external_module is None

    rec = mutable_database.get_record('externaltool')
    assert rec.spec.external_path == '/path/to/external_tool'
    assert rec.spec.external_module is None
    assert rec.explicit is False

    rec.spec.package.do_install(fake=True, explicit=True)
    rec = mutable_database.get_record('externaltool')
    assert rec.spec.external_path == '/path/to/external_tool'
    assert rec.spec.external_module is None
    assert rec.explicit is True


@pytest.mark.regression('8036')
def test_regression_issue_8036(mutable_database, usr_folder_exists):
    # The test ensures that the external package prefix is treated as
    # existing. Even when the package prefix exists, the package should
    # not be considered installed until it is added to the database with
    # do_install.
    s = spack.spec.Spec('externaltool@0.9')
    s.concretize()
    assert not s.package.installed

    # Now install the external package and check again the `installed` property
    s.package.do_install(fake=True)
    assert s.package.installed


@pytest.mark.regression('11118')
def test_old_external_entries_prefix(mutable_database):
    with open(spack.store.db._index_path, 'r') as f:
        db_obj = json.loads(f.read())

    s = spack.spec.Spec('externaltool')
    s.concretize()

    db_obj['database']['installs'][s.dag_hash()]['path'] = 'None'

    with open(spack.store.db._index_path, 'w') as f:
        f.write(json.dumps(db_obj))

    record = spack.store.db.get_record(s)

    assert record.path is None
    assert record.spec._prefix is None
    assert record.spec.prefix == record.spec.external_path


def test_uninstall_by_spec(mutable_database):
    with mutable_database.write_transaction():
        for spec in mutable_database.query():
            if spec.package.installed:
                spack.package.PackageBase.uninstall_by_spec(spec, force=True)
            else:
                mutable_database.remove(spec)
    assert len(mutable_database.query()) == 0
