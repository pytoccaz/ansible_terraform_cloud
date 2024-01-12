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
module: tfc_workspace_vars_info

short_description: Terraform Cloud API module to list workspace vars.

version_added: 1.0.0

description:
  - This module allows you to list to the variables attached to a workspace.

options:
    workspace_id:
        description:
            - The ID of the workspace to list variables for.
        type: str
        required: yes
        aliases:
          - workspace

extends_documentation_fragment:
    - pytoccaz.terraform_cloud.tfc_options

author:
  - Olivier Bernard (@pytoccaz)
'''

EXAMPLES = '''
- name: Get a all the variables associated with a workspace
  tfc_workspace_vars_info:
    workspace_id: WORKSPACEID
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
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

RETURN = '''
data:
    description: A list of variables
    returned: on success
    type: list
    elements: dict
    sample:
        - id: var-eZqhsovhfuze
          attributes:
                key: var1
                value: val1
'''
import json
from ansible.module_utils.urls import open_url
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.basic import AnsibleModule

URL_WORKSPACE_VARS = "{url}/api/{version}/workspaces/{workspace_id}/vars"


class TerraformCloudError(Exception):
    pass


def get_workspace_vars(module_params):
    version = module_params.get('api_version')
    workspace_id = module_params.get('workspace_id')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    http_agent = module_params.get('http_agent')
    connection_timeout = module_params.get('connection_timeout')
    api_url = module_params.get('api_url')

    url = URL_WORKSPACE_VARS.format(
        url=api_url, version=version, workspace_id=workspace_id)

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
    Module tf_workspace_vars_info
    """

    argument_spec = dict(
        api_url=dict(type='str', aliases=[
                     'url'], default="https://app.terraform.io"),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        api_version=dict(type='str', aliases=['version'], default='v2'),
        workspace_id=dict(type='str', aliases=['workspace'], required=True),
        validate_certs=dict(type='bool', default=True),
        connection_timeout=dict(type='int', default=10),
        http_agent=dict(type='str', default='Ansible'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        result = get_workspace_vars(module.params)
    except TerraformCloudError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
