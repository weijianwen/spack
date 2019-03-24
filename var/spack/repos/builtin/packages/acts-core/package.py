# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ActsCore(CMakePackage):
    """
    A Common Tracking Software (ACTS)

    This project contains an experiment-independent set of track reconstruction
    tools. The main philosophy is to provide high-level track reconstruction
    modules that can be used for any tracking detector. The description of the
    tracking detector's geometry is optimized for efficient navigation and
    quick extrapolation of tracks. Converters for several common geometry
    description languages exist. Having a highly performant, yet largely
    customizable implementation of track reconstruction algorithms was a
    primary objective for the design of this toolset. Additionally, the
    applicability to real-life HEP experiments plays major role in the
    development process. Apart from algorithmic code, this project also
    provides an event data model for the description of track parameters and
    measurements.

    Key features of this project include: tracking geometry description which
    can be constructed from TGeo, DD4Hep, or GDML input, simple and efficient
    event data model, performant and highly flexible algorithms for track
    propagation and fitting, basic seed finding algorithms.
    """

    homepage = "http://acts.web.cern.ch/ACTS/"
    git      = "https://gitlab.cern.ch/acts/acts-core.git"

    version('develop', branch='master')
    version('0.8.2', commit='c5d7568714e69e7344582b93b8d24e45d6b81bf9')
    version('0.8.1', commit='289bdcc320f0b3ff1d792e29e462ec2d3ea15df6')
    version('0.8.0', commit='99eedb38f305e3a1cd99d9b4473241b7cd641fa9')  # Used by acts-framework

    # Variants that affect the core ACTS library
    variant('legacy', default=False, description='Build the Legacy package')
    variant('examples', default=False, description='Build the examples')
    variant('tests', default=False, description='Build the unit tests')
    variant('integration_tests', default=False, description='Build the integration tests')

    # Variants the enable / disable ACTS plugins
    variant('digitization', default=False, description='Build the geometric digitization plugin')
    variant('dd4hep', default=False, description='Build the DD4hep plugin')
    variant('identification', default=False, description='Build the Identification plugin')
    variant('json', default=False, description='Build the Json plugin')
    variant('material', default=False, description='Build the material plugin')
    variant('tgeo', default=False, description='Build the TGeo plugin')

    depends_on('cmake @3.7:', type='build')
    depends_on('boost @1.62: +program_options +test')
    depends_on('eigen @3.2.9:', type='build')
    depends_on('root @6.10: cxxstd=14', when='+tgeo @:0.8.0')
    depends_on('root @6.10:', when='+tgeo @0.8.1:')
    depends_on('dd4hep @1.2:', when='+dd4hep')

    def cmake_args(self):
        spec = self.spec
        cxxstd = spec['root'].variants['cxxstd'].value

        def cmake_variant(cmake_label, spack_variant):
            enabled = spec.satisfies('+' + spack_variant)
            return "-DACTS_BUILD_{0}={1}".format(cmake_label, enabled)

        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(cxxstd),
            cmake_variant("LEGACY", "legacy"),
            cmake_variant("EXAMPLES", "examples"),
            cmake_variant("TESTS", "tests"),
            cmake_variant("INTEGRATION_TESTS", "integration_tests"),
            cmake_variant("DIGITIZATION_PLUGIN", "digitization"),
            cmake_variant("DD4HEP_PLUGIN", "dd4hep"),
            cmake_variant("IDENTIFICATION", "identification"),
            cmake_variant("JSON_PLUGIN", "json"),
            cmake_variant("MATERIAL_PLUGIN", "material"),
            cmake_variant("TGEO_PLUGIN", "tgeo")
        ]
        return args
