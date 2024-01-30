#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Olivier Bernard (@pytoccaz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: hcp_workspace_update

short_description: Terraform Cloud API (HCP) module to update a workspace.

version_added: 2.0.0

description:
  - This module updates a workspace by Id or name and organization
  - See https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces#update-a-workspace

options:
    api_url:
        description:
            - Terraform cloud service url.
            - You should not change the value except for test purpose.
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

    workspace_id:
        description:
            - The ID of the workspace.
            - C(workspace_name) with C(organization) can be used as an alternative.
        type: str
        aliases:
          - id

    organization:
        description:
            - The name of the organization the workspace belongs to.
            - Use with C(workspace_name).
            - Mutually exclusive with C(workspace_id).
        type: str

    workspace_name:
        description:
            - The name of the workspace.
            - Use with C(organization).
            - Mutually exclusive with C(workspace_id).
        type: str
        aliases:
          - name

extends_documentation_fragment:
    - pytoccaz.terraform_cloud.tfc_options
    - pytoccaz.terraform_cloud.tfc_payload

author:
  - Olivier Bernard (@pytoccaz)
'''

EXAMPLES = '''
- name: Change workspace name by workspace Id with payload option
  hcp_workspace_update:
    workspace_id: "ws-c6FoAsJsrD5abMrS"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    payload:
      data:
        attributes:
          name: "New_wk_name"

- name: Change workspace name by workspace Id with data option
  hcp_workspace_update:
    workspace_id: "ws-c6FoAsJsrD5abMrS"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    data:
      attributes:
        name: "New_wk_name"

- name: Change workspace name by workspace Id with attributes option
  hcp_workspace_update:
    workspace_id: "ws-c6FoAsJsrD5abMrS"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    attributes:
      name: "New_wk_name"
'''

RETURN = '''
data:
    description:
        - The data attribute from HCP route C(PATCH /workspaces/:workspace_id) or C(PATCH /organizations/:organization_name/workspaces/:name)
    returned: success
    type: dict
'''
from ..module_utils.tfc import TfcClient, TfcError
from ansible.module_utils.basic import AnsibleModule

WORKSPACE_PATH_BY_WORKSPACES = "/workspaces/{workspace_id}"
WORKSPACE_PATH_BY_ORGANIZATIONS = "/organizations/{organization}/workspaces/{workspace_name}"


def patch_workspace(module_params):
    workspace_id = module_params.get('workspace_id')
    workspace_name = module_params.get('workspace_name')
    organization = module_params.get('organization')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    connection_timeout = module_params.get('connection_timeout')
    api_url = module_params.get('api_url')
    data = module_params.get('data')
    attributes = module_params.get('attributes')
    payload = module_params.get('payload')

    if workspace_id is not None:
        path = WORKSPACE_PATH_BY_WORKSPACES.format(workspace_id=workspace_id)
    else:
        path = WORKSPACE_PATH_BY_ORGANIZATIONS.format(
            workspace_name=workspace_name, organization=organization)

    if payload is not None:
        pass
    elif data is not None:
        payload = {"data": data}
    else:
        payload = {"data": {"attributes": attributes}}

    client = TfcClient(token, url=api_url)
    r = client.patch(path, json=payload, verify=validate_certs,
                     timeout=connection_timeout)

    return r


def main():
    """
    Module hcp_workspace_update
    """

    argument_spec = dict(
        api_url=dict(type='str', aliases=['url']),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        workspace_id=dict(type='str', aliases=['id']),
        workspace_name=dict(type='str', aliases=['name']),
        organization=dict(type='str'),
        validate_certs=dict(type='bool', default=True),
        connection_timeout=dict(type='int', default=10),
        data=dict(type='dict'),
        payload=dict(type='dict'),
        attributes=dict(type='dict'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        mutually_exclusive=(['payload', 'data', 'attributes'], [
                            'workspace_name', "workspace_id"], ['organization', "workspace_id"],),
        required_together=(['organization', 'workspace_name'],),
        required_one_of=(['payload', 'data', 'attributes'], [
                         'workspace_name', "workspace_id"],),
    )

    try:
        result = patch_workspace(module.params)
    except TfcError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
