# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for compilers.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/compilers.py
   :lines: 13-
"""


#: Properties for inclusion in other schemas
properties = {
    'compilers': {
        'type': 'array',
        'items': [{
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'compiler': {
                    'type': 'object',
                    'additionalProperties': False,
                    'required': [
                        'paths', 'spec', 'modules', 'operating_system'],
                    'properties': {
                        'paths': {
                            'type': 'object',
                            'required': ['cc', 'cxx', 'f77', 'fc'],
                            'additionalProperties': False,
                            'properties': {
                                'cc':  {'anyOf': [{'type': 'string'},
                                                  {'type': 'null'}]},
                                'cxx': {'anyOf': [{'type': 'string'},
                                                  {'type': 'null'}]},
                                'f77': {'anyOf': [{'type': 'string'},
                                                  {'type': 'null'}]},
                                'fc':  {'anyOf': [{'type': 'string'},
                                                  {'type': 'null'}]}}},
                        'flags': {
                            'type': 'object',
                            'additionalProperties': False,
                            'properties': {
                                'cflags': {'anyOf': [{'type': 'string'},
                                                     {'type': 'null'}]},
                                'cxxflags': {'anyOf': [{'type': 'string'},
                                                       {'type': 'null'}]},
                                'fflags': {'anyOf': [{'type': 'string'},
                                                     {'type': 'null'}]},
                                'cppflags': {'anyOf': [{'type': 'string'},
                                                       {'type': 'null'}]},
                                'ldflags': {'anyOf': [{'type': 'string'},
                                                      {'type': 'null'}]},
                                'ldlibs': {'anyOf': [{'type': 'string'},
                                                     {'type': 'null'}]}}},
                        'spec': {'type': 'string'},
                        'operating_system': {'type': 'string'},
                        'target': {'type': 'string'},
                        'alias': {'anyOf': [{'type': 'string'},
                                            {'type': 'null'}]},
                        'modules': {'anyOf': [{'type': 'string'},
                                              {'type': 'null'},
                                              {'type': 'array'}]},
                        'implicit_rpaths': {
                            'type': 'array',
                            'items': {'type': 'string'}
                        },
                        'environment': {
                            'type': 'object',
                            'default': {},
                            'additionalProperties': False,
                            'properties': {
                                'set': {
                                    'type': 'object',
                                    'patternProperties': {
                                        # Variable name
                                        r'\w[\w-]*': {
                                            'anyOf': [{'type': 'string'},
                                                      {'type': 'number'}]
                                        }
                                    }
                                },
                                'unset': {
                                    'type': 'object',
                                    'patternProperties': {
                                        # Variable name
                                        r'\w[\w-]*': {'type': 'null'}
                                    }
                                },
                                'prepend-path': {
                                    'type': 'object',
                                    'patternProperties': {
                                        # Variable name
                                        r'\w[\w-]*': {
                                            'anyOf': [{'type': 'string'},
                                                      {'type': 'number'}]
                                        }
                                    }
                                },
                                'append-path': {
                                    'type': 'object',
                                    'patternProperties': {
                                        # Variable name
                                        r'\w[\w-]*': {
                                            'anyOf': [{'type': 'string'},
                                                      {'type': 'number'}]
                                        }
                                    }
                                }
                            }
                        },
                        'extra_rpaths': {
                            'type': 'array',
                            'default': [],
                            'items': {'type': 'string'}
                        }
                    }
                }
            }
        }]
    }
}


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack compiler configuration file schema',
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}
