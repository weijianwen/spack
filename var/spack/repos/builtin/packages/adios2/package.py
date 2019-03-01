# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Adios2(CMakePackage):
    """Next generation of ADIOS developed in the Exascale Computing Program"""

    homepage = "https://www.olcf.ornl.gov/center-projects/adios/"
    url      = "https://github.com/ornladios/ADIOS2/archive/v2.0.0.tar.gz"
    git      = "https://github.com/ornladios/ADIOS2.git"

    maintainers = ['ax3l', 'chuckatkins']

    version('develop', branch='master')
    version('2.3.1', sha256='3bf81ccc20a7f2715935349336a76ba4c8402355e1dc3848fcd6f4c3c5931893')
    version('2.2.0', sha256='77058ea2ff7224dc02ea519733de42d89112cf21ffe7474fb2fa3c5696152948')
    version('2.1.0', sha256='d4df3b3035b4236b51c77b59d68e756e825834b2ea3cb17439927a027831453b')
    version('2.0.0', sha256='4eeedf4404824d8de6e4ef580b8a703c0aedb5c03f900f5ce6f85f0b35980135')

    variant('shared', default=True,
            description='Also build shared libraries')
    variant('mpi', default=True,
            description='Enable MPI')
    # transforms
    variant('bzip2', default=True,
            description='Enable BZip2 compression')
    variant('zfp', default=True,
            description='Enable ZFP compression')
    # sz is broken in 2.2.0: https://github.com/ornladios/ADIOS2/issues/705
    # variant('sz', default=True,
    #         description='Enable SZ compression')
    # transport engines
    variant('dataman', default=True,
            description='Enable the DataMan engine for WAN transports')
    # currently required by DataMan, optional in the future
    # variant('zeromq', default=False,
    #         description='Enable ZeroMQ for the DataMan engine')
    variant('hdf5', default=False,
            description='Enable the HDF5 engine')
    variant('adios1', default=False,
            description='Enable the ADIOS 1.x engine')
    # language bindings
    variant('python', default=True,
            description='Enable the Python >= 2.7 bindings')
    variant('fortran', default=True,
            description='Enable the Fortran bindings')

    # requires mature C++11 implementations
    conflicts('%gcc@:4.7')
    conflicts('%intel@:15')
    conflicts('%pgi@:14')

    # DataMan needs dlopen
    conflicts('+dataman', when='~shared')

    depends_on('cmake@3.6.0:', type='build')
    depends_on('pkgconfig', type='build', when='@2.2.0:')
    # The included ffs requires bison and flex but using them makes
    # the build fail due to an undefined reference.
    # depends_on('bison', type='build', when='@2.2.0:')
    # depends_on('flex', when='@2.2.0:')

    depends_on('mpi', when='+mpi')
    depends_on('zeromq', when='+dataman')

    depends_on('hdf5', when='+hdf5')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('adios', when='+adios1')
    depends_on('adios+mpi', when='+adios1+mpi')

    depends_on('bzip2', when='+bzip2')
    depends_on('zfp', when='+zfp')
    # depends_on('sz@:1.4.12', when='+sz')

    extends('python', when='+python')
    depends_on('python@2.7:', type=('build', 'run'), when='+python')
    depends_on('py-numpy@1.6.1:', type=('build', 'run'), when='+python')
    depends_on('py-mpi4py@2.0.0:', type=('build', 'run'), when='+mpi +python')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DADIOS2_BUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-DADIOS2_BUILD_TESTING=OFF',
            '-DADIOS2_USE_MPI={0}'.format(
                'ON' if '+mpi' in spec else 'OFF'),
            '-DADIOS2_USE_BZip2={0}'.format(
                'ON' if '+bzip2' in spec else 'OFF'),
            '-DADIOS2_USE_ZFP={0}'.format(
                'ON' if '+zfp' in spec else 'OFF'),
            '-DADIOS2_USE_SZ={0}'.format(
                'ON' if '+sz' in spec else 'OFF'),
            '-DADIOS2_USE_DataMan={0}'.format(
                'ON' if '+dataman' in spec else 'OFF'),
            '-DADIOS2_USE_ZeroMQ={0}'.format(
                'ON' if '+dataman' in spec else 'OFF'),
            '-DADIOS2_USE_HDF5={0}'.format(
                'ON' if '+hdf5' in spec else 'OFF'),
            '-DADIOS2_USE_ADIOS1={0}'.format(
                'ON' if '+adios1' in spec else 'OFF'),
            '-DADIOS2_USE_Python={0}'.format(
                'ON' if '+python' in spec else 'OFF'),
            '-DADIOS2_USE_Fortran={0}'.format(
                'ON' if '+fortran' in spec else 'OFF')
        ]
        if spec.satisfies('+python'):
            args.append('-DPYTHON_EXECUTABLE:FILEPATH=%s'
                        % self.spec['python'].command.path)
        return args
