#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Olivier Bernard (@pytoccaz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: tfc_workspace_var_create

short_description: Terraform Cloud API (HCP Terraform) module to create a workspace variable.

version_added: 2.2.0

description:
  - This module creates a variable attached to a workspace.
  - See https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables#create-a-variable

options:
    workspace_id:
        description:
            - The ID of the workspace which the variable is associated.
        type: str
        required: true

extends_documentation_fragment:
    - pytoccaz.terraform_cloud.tfc_options
    - pytoccaz.terraform_cloud.tfc_payload

author:
  - Olivier Bernard (@pytoccaz)
'''

EXAMPLES = '''
- name: Create a variable
  tfc_workspace_var_create:
    workspace_id: "ws-c6FoAsJsrD5abMrS"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    attributes:
      key: "var_name"
      value: "value1"
'''

RETURN = '''
data:
    description:
        - The data attribute from HCP Terraform route C(POST /workspaces/:workspace_id/vars)
    returned: success
    type: dict
'''
from ..module_utils.tfc import TfcClient, TfcError
from ansible.module_utils.basic import AnsibleModule

WORKSPACE_VARS_PATH = "/workspaces/{workspace_id}/vars"


def create_var(module_params):
    api_url = module_params.get('api_url')
    workspace_id = module_params.get('workspace_id')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    connection_timeout = module_params.get('connection_timeout')
    data = module_params.get('data')
    attributes = module_params.get('attributes')
    payload = module_params.get('payload')

    if payload is not None:
        pass
    elif data is not None:
        payload = {"data": {"type": "vars", **data}}
    else:
        payload = {"data": {"type": "vars", "attributes": { "category": "terraform", **attributes }}}

    client = TfcClient(token, url=api_url)
    
    path = WORKSPACE_VARS_PATH.format(workspace_id=workspace_id)

    r = client.create(path, json=payload, verify=validate_certs,
                     timeout=connection_timeout)

    return r


def main():
    """
    Module tfc_workspace_var_create
    """

    argument_spec = dict(
        api_url=dict(type='str', aliases=['url']),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        workspace_id=dict(type='str', required=True),
        validate_certs=dict(type='bool', default=True),
        connection_timeout=dict(type='int', default=10),
        data=dict(type='dict'),
        payload=dict(type='dict'),
        attributes=dict(type='dict'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=(['payload', 'data', 'attributes'],),
        required_one_of=(['payload', 'data', 'attributes'],),
    )

    try:
        result = create_var(module.params)
    except TfcError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
