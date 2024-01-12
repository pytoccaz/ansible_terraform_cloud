# -*- coding: utf-8 -*-

# Copyright: (c) 2024 Olivier Bernard
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # doc fragment
    DOCUMENTATION = r'''

options:
    api_version:
        description:
            - The version of Terraform Cloud API.
            - The version C(v2) is currently the only possible value, so you should not change it.
        type: str
        default: v2
        aliases:
          - version

    api_url:
        description:
            - Terraform cloud service url.
            - You should not change the value unless for test purpose.
        type: str
        default: https://app.terraform.io
        aliases:
            - url

    api_token:
        description:
            - A token to authenticate Ansible.
        type: str
        required: yes
        aliases:
            - token

    validate_certs:
        description:
            - Verify TLS certificates (do not disable this in production).
        type: bool
        default: true

    connection_timeout:
        description:
            - Controls the HTTP connections timeout period (in seconds) to the API.
        type: int
        default: 10

    http_agent:
        description:
            - Configures the HTTP User-Agent header.
        type: str
        default: Ansible
    '''
