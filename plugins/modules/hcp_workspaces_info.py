#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Olivier Bernard (@pytoccaz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: hcp_workspaces_info

short_description: Terraform Cloud API (HCP) module to lists workspaces in one organization.

version_added: 1.0.0

description:
    - This module lists the workspaces in one organization the appropriate Terraform Cloud API (HCP) endpoint.
    - See https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces#list-workspaces.
options:
    organization:
        description:
            - The name of the organization the workspace belongs to.
        type: str
        required: yes

    page_number:
        description:
            - Pagination page number.
        type: int
        default: 1
        aliases:
          - page

    page_size:
        description:
            - Pagination page size.
        type: int
        default: 20
        aliases:
          - size

    search_name:
        description:
            - Restricts results to workspaces with a name that matches the search string using a fuzzy search.
        type: str

    search_wildcard_name:
        description:
            - Restricts restricts results to workspaces with partial matching, using * on prefix, suffix, or both.
        type: str
        aliases:
          - search_wildcard

extends_documentation_fragment:
    - pytoccaz.terraform_cloud.tfc_options

author:
  - Olivier Bernard (@pytoccaz)
'''

EXAMPLES = '''
  - name: Get the first 10 workspaces from Terraform Cloud for orga myorga
    tfc_workspaces_info:
      organization: myorga
      page_size: 10
      token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
'''

RETURN = '''
    data:
        description:
            - The data attribute from HCP route C(GET /organizations/:organization_name/workspaces/:name).
        returned: success
        type: list
        elements: dict
'''
from ..module_utils.tfc import TfcClient, TfcError
from ansible.module_utils.basic import AnsibleModule

WORKSPACES_PATH = "/organizations/{organization}/workspaces"


def get_workspaces(module_params):
    organization = module_params.get('organization')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    connection_timeout = module_params.get('connection_timeout')
    api_url = module_params.get('api_url')
    page_number = module_params.get('page_number')
    size = module_params.get('page_size')
    direct_link = module_params.get('direct_link')
    search_name = module_params.get('search_name')
    search_wildcard = module_params.get('search_wildcard_name')

    params = None

    if direct_link is not None:
        path = direct_link
    else:
        path = WORKSPACES_PATH.format(organization=organization)
        params = [('page[number]', page_number), ('page[size]', size)]

        if search_name is not None:
            params.append(('search[name]', search_name))
        elif search_wildcard is not None:
            params.append(('search[wildcard-name]', search_wildcard))

    client = TfcClient(token, url=api_url)
    r = client.read(path, params=params, verify=validate_certs,
                    timeout=connection_timeout)

    return r


def main():
    """
    Module tfc_workspaces_info
    """

    argument_spec = dict(
        direct_link=dict(type='str', aliases=['link']),
        organization=dict(type='str', required=True),
        api_url=dict(type='str', aliases=[
                     'url'], default="https://app.terraform.io"),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        page_number=dict(type='int', aliases=['page'], default=1),
        page_size=dict(type='int', aliases=['size'], default=20),
        validate_certs=dict(type='bool', default=True),
        search_name=dict(type='str'),
        search_wildcard_name=dict(type='str', aliases=['search_wildcard']),
        connection_timeout=dict(type='int', default=10),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=([
                            ['direct_link', 'page_number'],
                            ['direct_link', 'page_size'],
                            ['direct_link', 'search_name'],
                            ['direct_link', 'search_wildcard_name'],
                            ['search_name', 'search_wildcard_name'],
                            ]),
    )

    try:
        result = get_workspaces(module.params)
    except TfcError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
