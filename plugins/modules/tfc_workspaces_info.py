#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Olivier Bernard (@pytoccaz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is inspired by and contains code snippets from:
# - `community.general.plugins.module_utils.identity.keycloak.keycloak` module by Eike Frost
# - `community.general.plugins.module_utils.identity.keycloak.keycloak_clientsecret` module by John Cant
# - `community.general.plugins.modules.keycloak_clientsecret_info` module by Fynn Chen
# It also contains documentation fragments from `community.general.doc_fragments.keycloak` by Eike Frost.

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: tfc_workspaces_info

short_description: Terraform Cloud API module to lists workspaces in a organization.

version_added: 1.0.0

description:
  - This module allows you to list to workspaces in a organization via
    the Terraform Cloud API workspaces endpoint.

options:
    direct_link:
        description:
            - A complet link with urlencoded parameters for pagination or search filters.
        type: str
        aliases:
            - link

    organization:
        description:
            - The organization name.
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
- name: Get a the first workspace from Terraform Cloud for orga myorga
  tfc_workspaces_info:
    organization: myorga
    page_size: 1
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
  register: a_workspace
'''

RETURN = '''
data:
    description: The workspaces list
    returned: on success
    type: list
    elements: dict
links:
    description: The pagination links
    returned: on success
    type: list
    elements: dict

meta:
    description: Pagination info
    returned: on success
    type: dict
'''
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.urls import open_url
import json


URL_WORKSPACES = "{url}/api/{version}/organizations/{organization}/workspaces?{params}"


class TerraformCloudError(Exception):
    pass


def get_workspaces(module_params):
    version = module_params.get('api_version')
    organization = module_params.get('organization')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    http_agent = module_params.get('http_agent')
    connection_timeout = module_params.get('connection_timeout')
    api_url = module_params.get('api_url')
    page_number = module_params.get('page_number')
    size = module_params.get('page_size')
    direct_link = module_params.get('direct_link')
    search_name = module_params.get('search_name')
    search_wildcard = module_params.get('search_wildcard_name')

    if direct_link is not None:
        url = direct_link
    else:
        params = [('page[number]', page_number), ('page[size]', size)]

        if search_name is not None:
            params.append(('search[name]', search_name))
        elif search_wildcard is not None:
            params.append(('search[wildcard-name]', search_wildcard))

        url = URL_WORKSPACES.format(
            url=api_url, version=version, organization=organization, params=urlencode(params))

    if not url.lower().startswith(('http', 'https')):
        raise TerraformCloudError(
            "url '%s' should either start with 'http' or 'https'." % url)

    headers = {
        'Authorization': "Bearer {token}".format(token=token)
    }

    try:
        r = json.loads(to_native(open_url(url, method='GET', headers=headers,
                                          validate_certs=validate_certs, http_agent=http_agent, timeout=connection_timeout,
                                          #   data=urlencode(payload)
                                          ).read()))
    except ValueError as e:
        raise TerraformCloudError(
            'API returned invalid JSON when trying to get %s: %s'
            % (url, str(e)))
    except Exception as e:
        raise TerraformCloudError('Response error from %s: %s'
                                  % (url, str(e)))

    return r


def main():
    """
    Module tf_workspaces_info
    """

    argument_spec = dict(
        direct_link=dict(type='str', aliases=['link']),
        organization=dict(type='str', required=True),
        api_url=dict(type='str', aliases=[
                     'url'], default="https://app.terraform.io"),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        api_version=dict(type='str', aliases=['version'], default='v2'),
        page_number=dict(type='int', aliases=['page'], default=1),
        page_size=dict(type='int', aliases=['size'], default=20),
        validate_certs=dict(type='bool', default=True),
        search_name=dict(type='str'),
        search_wildcard_name=dict(type='str', aliases=['search_wildcard']),
        connection_timeout=dict(type='int', default=10),
        http_agent=dict(type='str', default='Ansible'),
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
    except TerraformCloudError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
