# -*- coding: utf-8 -*-

# Copyright: (c) 2024 Olivier Bernard
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # doc fragment
    DOCUMENTATION = r'''

options:
    payload:
        description:
            - Raw payload containing usually a C(data) property
            - Mutually exclusive with options C(data) and C(attributes)
        type: dict
    data:
        description:
            - data content (usually an C(attributes) property)
            - shortcut for plain C(payload) option
            - Mutually exclusive with options C(payload) and C(attributes)
        type: dict
    attributes:
        description:
            - attributes content
            - shortcut for C(data) option
            - Mutually exclusive with options C(payload) and C(data)
        type: dict
    '''
