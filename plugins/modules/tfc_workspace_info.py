#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Olivier Bernard (@pytoccaz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
---
module: tfc_workspace_info

short_description: Terraform Cloud API (HCP Terraform) module to display a workspace.

version_added: 1.0.0

description:
  - This module gives detail about one particuliar workspace given its ID or workspace name and organization.
  - See https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces#show-workspace.

options:
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

author:
  - Olivier Bernard (@pytoccaz)
'''

EXAMPLES = '''
- name: Get a workspace given the ID
  tfc_workspaces_info:
    workspace_id: "ws-c6FoAsJsrD5abMrS"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"

- name: Get a workspace given name and organization
  tfc_workspaces_info:
    workspace_name: "test"
    organization: "MyOrga"
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
'''

RETURN = '''
data:
    description:
        - The data attribute from HCP Terraform route C(GET /workspaces/:workspace_id) or C(GET /organizations/:organization_name/workspaces/:name).
    returned: success
    type: dict
'''
from ..module_utils.tfc import TfcClient, TfcError
from ansible.module_utils.basic import AnsibleModule

WORKSPACE_PATH_BY_WORKSPACES = "/workspaces/{workspace_id}"
WORKSPACE_PATH_BY_ORGANIZATIONS = "/organizations/{organization}/workspaces/{workspace_name}"


def get_workspace(module_params):
    workspace_id = module_params.get('workspace_id')
    workspace_name = module_params.get('workspace_name')
    organization = module_params.get('organization')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    connection_timeout = module_params.get('connection_timeout')
    api_url = module_params.get('api_url')

    if workspace_id is not None:
        path = WORKSPACE_PATH_BY_WORKSPACES.format(workspace_id=workspace_id)
    else:
        path = WORKSPACE_PATH_BY_ORGANIZATIONS.format(
            workspace_name=workspace_name, organization=organization)

    client = TfcClient(token, url=api_url)
    r = client.read(path, verify=validate_certs, timeout=connection_timeout)

    return r


def main():
    """
    Module tfc_workspace_info
    """

    argument_spec = dict(
        workspace_id=dict(type='str', aliases=['id']),
        workspace_name=dict(type='str', aliases=['name']),
        organization=dict(type='str'),
        api_url=dict(type='str', aliases=['url']),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        validate_certs=dict(type='bool', default=True),
        connection_timeout=dict(type='int', default=10),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=(['workspace_name', "workspace_id"], [
                            'organization', "workspace_id"],),
        required_together=(['organization', 'workspace_name'],),
        required_one_of=(['workspace_name', "workspace_id"],),
    )

    try:
        result = get_workspace(module.params)
    except TfcError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
