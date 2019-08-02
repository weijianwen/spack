# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for env.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/env.py
   :lines: 36-
"""
from llnl.util.lang import union_dicts

import spack.schema.merged
import spack.schema.projections


spec_list_schema = {
    'type': 'array',
    'default': [],
    'items': {
        'anyOf': [
            {'type': 'object',
             'additionalProperties': False,
             'properties': {
                 'matrix': {
                     'type': 'array',
                     'items': {
                         'type': 'array',
                         'items': {
                             'type': 'string',
                         }
                     }
                 },
                 'exclude': {
                     'type': 'array',
                     'items': {
                         'type': 'string'
                     }
                 }
             }},
            {'type': 'string'},
            {'type': 'null'}
        ]
    }
}

projections_scheme = spack.schema.projections.properties['projections']

schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack environment file schema',
    'type': 'object',
    'additionalProperties': False,
    'patternProperties': {
        '^env|spack$': {
            'type': 'object',
            'default': {},
            'additionalProperties': False,
            'properties': union_dicts(
                # merged configuration scope schemas
                spack.schema.merged.properties,
                # extra environment schema properties
                {
                    'include': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                    },
                    'definitions': {
                        'type': 'array',
                        'default': [],
                        'items': {
                            'type': 'object',
                            'properties': {
                                'when': {
                                    'type': 'string'
                                }
                            },
                            'patternProperties': {
                               r'^(?!when$)\w*': spec_list_schema
                            }
                        }
                    },
                    'specs': spec_list_schema,
                    'view': {
                        'anyOf': [
                            {'type': 'boolean'},
                            {'type': 'string'},
                            {'type': 'object',
                             'patternProperties': {
                                  r'\w+': {
                                      'required': ['root'],
                                      'additionalProperties': False,
                                      'properties': {
                                          'root': {
                                              'type': 'string'
                                          },
                                          'link': {
                                              'type': 'string',
                                              'pattern': '(roots|all)',
                                          },
                                          'select': {
                                              'type': 'array',
                                              'items': {
                                                  'type': 'string'
                                              }
                                          },
                                          'exclude': {
                                              'type': 'array',
                                              'items': {
                                                  'type': 'string'
                                              }
                                        },
                                          'projections': projections_scheme
                                      }
                                  }
                             }
                            }
                        ]
                    }
                }
            )
        }
    }
}
