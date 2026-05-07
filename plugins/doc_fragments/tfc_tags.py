# -*- coding: utf-8 -*-

# Copyright: (c) 2024 Olivier Bernard
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # doc fragment
    DOCUMENTATION = r'''

options:
    tags:
        description:
            - key-value list of tags
            - Mutually exclusive with options C(payload) ans C(data)
        type: dict       
    '''
