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

short_description: Terraform Cloud API module to show details on a workspace.

version_added: 1.1.0

description:
  - This module allows you to show to the details of a workspace.
  - The workspace is defined by it's Id or by it's organization and name.

options:
    workspace_id:
        description:
            - The ID of the workspace.
            - O(workspace_name) with O(organization) can be used as an alternative.
        type: str
        aliases:
          - id

    organization:
        description:
            - The name of the organization the workspace belongs to.
            - Use with O(workspace_name).
            - Mutually exclusive with O(workspace_id).
        type: str

    workspace_name:
        description:
            - The name of the workspace.
            - Use with O(organization).
            - Mutually exclusive with O(workspace_id).
        type: str
        aliases:
          - name

extends_documentation_fragment:
    - pytoccaz.terraform_cloud.tfc_options

author:
  - Olivier Bernard (@pytoccaz)
'''

EXAMPLES = '''
- name: Retrieve workspace details by workspace Id
  tfc_workspace_info:
    workspace_id: WORKSPACEID
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
    
    
- name: Retrieve workspace details by workspace organization and name
  tfc_workspace_info:
    workspace_name: workspace1
    organization: orga1
    token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
'''

RETURN = '''
data:
    description: The workspace details
    returned: on success
    type: dict
'''

RETURN = '''
data:
    description: The workspace details
    returned: on success
    type: dict
    sample:
        id: ws-4YD4Y4sIDnl8PpV2
        attributes:
            name: workspace1
'''
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.urls import open_url
import json


URL_WORKSPACE_ID = "{url}/api/{version}/workspaces/{workspace_id}"

URL_WORKSPACE_NAME = "{url}/api/{version}/organizations/{organization}/workspaces/{workspace_name}"


class TerraformCloudError(Exception):
    pass


def get_workspace_by_id(module_params):
    version = module_params.get('api_version')
    workspace_id = module_params.get('workspace_id')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    http_agent = module_params.get('http_agent')
    connection_timeout = module_params.get('connection_timeout')
    api_url = module_params.get('api_url')

    url = URL_WORKSPACE_ID.format(
        url=api_url, version=version, workspace_id=workspace_id)

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


def get_workspace_by_name(module_params):
    version = module_params.get('api_version')
    workspace_name = module_params.get('workspace_name')
    organization = module_params.get('organization')
    validate_certs = module_params.get('validate_certs')
    token = module_params.get('api_token')
    http_agent = module_params.get('http_agent')
    connection_timeout = module_params.get('connection_timeout')
    api_url = module_params.get('api_url')

    url = URL_WORKSPACE_NAME.format(
        url=api_url, version=version, workspace_name=workspace_name, organization=organization)

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


def get_workspace_info(module_params):
    workspace_id = module_params.get('workspace_id')
    workspace_name = module_params.get('workspace_name')
    api_url = module_params.get('api_url')

    if not api_url.lower().startswith(('http', 'https')):
        raise TerraformCloudError(
            "url '%s' should either start with 'http' or 'https'." % api_url)

    if workspace_id is not None:
        return get_workspace_by_id(module_params)

    if workspace_name is not None:
        return get_workspace_by_name(module_params)


def main():
    """
    Module tf_workspace_info
    """

    argument_spec = dict(
        api_url=dict(type='str', aliases=[
                     'url'], default="https://app.terraform.io"),
        api_token=dict(type='str', aliases=[
                       'token'], required=True, no_log=True),
        api_version=dict(type='str', aliases=['version'], default='v2'),
        workspace_id=dict(type='str', aliases=['id']),
        organization=dict(type='str'),
        workspace_name=dict(type='str', aliases=['name']),
        validate_certs=dict(type='bool', default=True),
        connection_timeout=dict(type='int', default=10),
        http_agent=dict(type='str', default='Ansible'),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ('workspace_id', 'workspace_name'),
            ('workspace_id', 'organization'),
        ],
        required_together=[('workspace_name', 'organization')],
        required_one_of=[('workspace_id', 'workspace_name')],
    )

    try:
        result = get_workspace_info(module.params)
    except TerraformCloudError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
