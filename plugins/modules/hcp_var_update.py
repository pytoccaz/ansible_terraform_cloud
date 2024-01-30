#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Olivier Bernard (@pytoccaz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: hcp_var_update

short_description: Terraform Cloud API (HCP) module to list workspace vars.

version_added: 2.0.0

description:
    - This module modifies a variable given the ID.
    - This module is an alternative to C(hcp_workspace_var_update).
    - See https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variables#update-variables

seealso:
    - module: pytoccaz.terraform_cloud.hcp_workspace_var_update

options:
    variable_id:
        description:
            - The ID of the variable to update.
        type: str
        required: yes
        aliases:
          - id

extends_documentation_fragment:
    - pytoccaz.terraform_cloud.tfc_options
    - pytoccaz.terraform_cloud.tfc_payload

author:
  - Olivier Bernard (@pytoccaz)
'''

EXAMPLES = '''
- name: Change the value of a variable with payload option
  hcp_var_update:
    variable_id: "var-sQaLVxPGd8Bhui56"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    payload:
      data:
        attributes:
          value: "var10"

- name: Change the value of a variable with data option
  hcp_var_update:
    variable_id: "var-sQaLVxPGd8Bhui56"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    data:
      attributes:
        value: "var10"

- name: Change the value of a variable with attributes option
  hcp_var_update:
    variable_id: "var-sQaLVxPGd8Bhui56"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    attributes:
      value: "var10"
'''

RETURN = '''
data:
    description:
        - The data attribute from HCP route C(PATCH /vars/:variable_id)
    returned: success
    type: dict
'''
from ..module_utils.tfc import TfcClient, TfcError
from ansible.module_utils.basic import AnsibleModule

WORKSPACE_VAR_PATH = "/vars/{variable_id}"


def update_var(module_params):
    api_url = module_params.get('api_url')
    variable_id = module_params.get('variable_id')
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

    path = WORKSPACE_VAR_PATH.format(variable_id=variable_id)

    client = TfcClient(token, url=api_url)
    r = client.patch(path, json=payload, verify=validate_certs,
                     timeout=connection_timeout)

    return r


def main():
    """
    Module hcp_var_update
    """

    argument_spec = dict(
        api_url=dict(type='str', aliases=['url']),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        variable_id=dict(type='str', aliases=['id'], required=True),
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
        result = update_var(module.params)
    except TfcError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
