#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Olivier Bernard (@pytoccaz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: tfc_workspace_var_update

short_description: Terraform Cloud API (HCP Terraform) module to modify workspace vars.

version_added: 2.0.0

description:
  - This module modifies a variable attached to a workspace.
  - This module is an alternative to C(tfc_var_update).
  - See https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspace-variables#update-variables

options:
    workspace_id:
        description:
            - The ID of the workspace which the variable is associated.
        type: str
        required: true

    variable_id:
        description:
            - The ID of the variable to update.
            - Mutually exclusive with C(key) option.
        type: str

    variable_key:
        description:
            - The key of the variable to update.
            - Alternative to C(variable_id) for better convenience.
        type: str
        aliases:
            - key

extends_documentation_fragment:
    - pytoccaz.terraform_cloud.tfc_options
    - pytoccaz.terraform_cloud.tfc_payload

author:
  - Olivier Bernard (@pytoccaz)
'''

EXAMPLES = '''
- name: Change the value of a variable by variable ID
  tfc_workspace_var_update:
    workspace_id: "ws-c6FoAsJsrD5abMrS"
    variable_id: "var-sQaLVxPGd8Bhui56"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    payload:
      data:
        attributes:
          value: "value1"

- name: Change the value of a variable by variable key
  tfc_workspace_var_update:
    workspace_id: "ws-c6FoAsJsrD5abMrS"
    variable_key: "var1"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    data:
      attributes:
        value: "value1"
'''

RETURN = '''
data:
    description:
        - The data attribute from HCP Terraform route C(PATCH /workspaces/:workspace_id/vars/:variable_id)
    returned: success
    type: dict
'''
from ..module_utils.tfc import TfcClient, TfcError
from ansible.module_utils.basic import AnsibleModule

WORKSPACE_VAR_PATH = "/workspaces/{workspace_id}/vars/{variable_id}"
WORKSPACE_VARS_PATH = "/workspaces/{workspace_id}/vars"


def update_var(module_params):
    api_url = module_params.get('api_url')
    workspace_id = module_params.get('workspace_id')
    variable_id = module_params.get('variable_id')
    variable_key = module_params.get('variable_key')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    connection_timeout = module_params.get('connection_timeout')
    data = module_params.get('data')
    attributes = module_params.get('attributes')
    payload = module_params.get('payload')

    if payload is not None:
        pass
    elif data is not None:
        payload = {"data": data}
    else:
        payload = {"data": {"attributes": attributes}}

    client = TfcClient(token, url=api_url)

    if variable_key is not None:
        path = WORKSPACE_VARS_PATH.format(workspace_id=workspace_id)
        vars = client.read(path, verify=validate_certs,
                           timeout=connection_timeout)

        try:
            variable_id = list(filter(
                lambda var: var["attributes"]["key"] == variable_key, vars["data"]))[0]["id"]
        except IndexError as e:
            raise TfcError('Variable with key %s not found.' % (variable_key))

    path = WORKSPACE_VAR_PATH.format(
        workspace_id=workspace_id, variable_id=variable_id)

    r = client.patch(path, json=payload, verify=validate_certs,
                     timeout=connection_timeout)

    return r


def main():
    """
    Module tfc_workspace_var_update
    """

    argument_spec = dict(
        api_url=dict(type='str', aliases=['url']),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        variable_id=dict(type='str'),
        variable_key=dict(type='str', aliases=['key'], no_log=False),
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
        mutually_exclusive=(['payload', 'data', 'attributes'], [
                            'variable_key', 'variable_id']),
        required_one_of=(['payload', 'data', 'attributes'],
                         ['variable_key', 'variable_id']),
    )

    try:
        result = update_var(module.params)
    except TfcError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
