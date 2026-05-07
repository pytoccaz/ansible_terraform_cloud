#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 Olivier Bernard (@pytoccaz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
from ..module_utils.tfc import TfcClient, TfcError, add_tags

__metaclass__ = type


DOCUMENTATION = '''
---
module: tfc_project_update

short_description: Terraform Cloud API (HCP Terraform) module to update a project.

version_added: 2.2.0

description:
  - This module update a project inside an organization
  - See https://developer.hashicorp.com/terraform/cloud-docs/api-docs/projects#update-a-project

options:
    project_id:
        description:
            - The project Id.
        type: str

extends_documentation_fragment:
    - pytoccaz.terraform_cloud.tfc_options
    - pytoccaz.terraform_cloud.tfc_payload
    - pytoccaz.terraform_cloud.tfc_tags

author:
  - Olivier Bernard (@pytoccaz)
'''

EXAMPLES = '''
- name: Update a project
  tfc_project_update:
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    project_id: prj-ENPobeXyhdHXZh6kh
    payload:
      data:
        attributes:
          type: "project"
          name: "New_project_name"
'''

RETURN = '''
data:
    description:
        - The data attribute from HCP Terraform route C(POST /projects/:project_id)
    returned: success
    type: dict
'''

PROJECT_PATH = "/projects/{project_id}"


def update_project(module_params):
    project_id = module_params.get('project_id')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    connection_timeout = module_params.get('connection_timeout')
    api_url = module_params.get('api_url')
    data = module_params.get('data')
    attributes = module_params.get('attributes')
    payload = module_params.get('payload')
    tags = module_params.get('tags')

    path = PROJECT_PATH.format(project_id=project_id)

    if payload is not None:
        pass
    elif data is not None:
        payload = {"data": {"type": "projects", **data}}
    else:
        payload = { "data": {"type": "projects"} }
    
    if attributes is not None:
        payload["data"]["attributes"] = attributes
    if tags is not None:
        add_tags(payload, tags)



    client = TfcClient(token, url=api_url)
    r = client.patch(path, json=payload, verify=validate_certs,
                      timeout=connection_timeout)

    return r


def main():
    """
    Module tfc_project_update
    """

    argument_spec = dict(
        api_url=dict(type='str', aliases=['url']),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        project_id=dict(type='str', required=True),
        validate_certs=dict(type='bool', default=True),
        connection_timeout=dict(type='int', default=10),
        data=dict(type='dict'),
        payload=dict(type='dict'),
        attributes=dict(type='dict'),
        tags=dict(type='dict'), 
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        mutually_exclusive=(['payload', 'data', 'attributes'], ['payload', 'data', 'tags']),
        required_one_of=(['payload', 'data', 'attributes', 'tags'],),
    )

    try:
        result = update_project(module.params)
    except TfcError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
