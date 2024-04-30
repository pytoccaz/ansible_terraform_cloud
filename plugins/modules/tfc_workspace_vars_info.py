#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Olivier Bernard (@pytoccaz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: tfc_workspace_vars_info

short_description: Terraform Cloud API (HCP Terraform) module to list workspace vars.

version_added: 1.0.0

description:
  - Lists the variables attached to a workspace.
  - See https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables#list-variables

options:
    workspace_id:
        description:
            - The ID of the workspace to list variables for.
        type: str
        required: yes
        aliases:
          - id

extends_documentation_fragment:
    - pytoccaz.terraform_cloud.tfc_options

author:
  - Olivier Bernard (@pytoccaz)
'''

EXAMPLES = '''
- name: List all the variables attached to a workspace
  tfc_workspace_vars_info:
    workspace_id: "ws-c6FoAsJsrD5abMrS"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
'''

RETURN = '''
data:
    description:
        - The data attribute from HCP Terraform route C(GET /workspaces/:workspace_id/vars)
    returned: success
    type: list
    elements: dict
'''
from ..module_utils.tfc import TfcClient, TfcError
from ansible.module_utils.basic import AnsibleModule

WORKSPACE_VARS_PATH = "/workspaces/{workspace_id}/vars"


def get_workspace_vars(module_params):
    workspace_id = module_params.get('workspace_id')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    connection_timeout = module_params.get('connection_timeout')
    api_url = module_params.get('api_url')

    path = WORKSPACE_VARS_PATH.format(workspace_id=workspace_id)

    client = TfcClient(token, url=api_url)
    r = client.read(path, verify=validate_certs, timeout=connection_timeout)

    return r


def main():
    """
    Module tfc_workspace_vars_info
    """

    argument_spec = dict(
        api_url=dict(type='str', aliases=['url']),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        workspace_id=dict(type='str', aliases=['id'], required=True),
        validate_certs=dict(type='bool', default=True),
        connection_timeout=dict(type='int', default=10),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        result = get_workspace_vars(module.params)
    except TfcError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
