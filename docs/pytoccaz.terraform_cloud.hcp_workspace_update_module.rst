.. _pytoccaz.terraform_cloud.hcp_workspace_update_module:


*********************************************
pytoccaz.terraform_cloud.hcp_workspace_update
*********************************************

**Terraform Cloud API (HCP) module to update a workspace.**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module updates a workspace by Id or name and organization
- See https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces#update-a-workspace




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>api_token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A token to authenticate Ansible.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: token</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>api_url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"https://app.terraform.io"</div>
                </td>
                <td>
                        <div>Terraform cloud service url.</div>
                        <div>You should not change the value except for test purpose.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: url</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>attributes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>attributes content</div>
                        <div>shortcut for <code>data</code> option</div>
                        <div>Mutually exclusive with options <code>payload</code> and <code>data</code></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>connection_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">10</div>
                </td>
                <td>
                        <div>Controls the HTTP connections timeout period (in seconds) to the API.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>data content (usually an <code>attributes</code> property)</div>
                        <div>shortcut for plain <code>payload</code> option</div>
                        <div>Mutually exclusive with options <code>payload</code> and <code>attributes</code></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>organization</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the organization the workspace belongs to.</div>
                        <div>Use with <code>workspace_name</code>.</div>
                        <div>Mutually exclusive with <code>workspace_id</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>payload</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Raw payload containing usually a <code>data</code> property</div>
                        <div>Mutually exclusive with options <code>data</code> and <code>attributes</code></div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: raw</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>validate_certs</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Verify TLS certificates (do not disable this in production).</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>workspace_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The ID of the workspace.</div>
                        <div><code>workspace_name</code> with <code>organization</code> can be used as an alternative.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: id</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>workspace_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the workspace.</div>
                        <div>Use with <code>organization</code>.</div>
                        <div>Mutually exclusive with <code>workspace_id</code>.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: name</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

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



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>The data attribute from HCP route <code>PATCH /workspaces/:workspace_id</code> or <code>PATCH /organizations/:organization_name/workspaces/:name</code></div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Olivier Bernard (@pytoccaz)
