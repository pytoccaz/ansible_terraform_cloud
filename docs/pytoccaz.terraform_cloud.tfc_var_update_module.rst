.. _pytoccaz.terraform_cloud.tfc_var_update_module:


***************************************
pytoccaz.terraform_cloud.tfc_var_update
***************************************

**Terraform Cloud API (HCP Terraform) module to list workspace vars.**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module modifies a variable given the variable ID.
- This module is an alternative to ``tfc_workspace_var_update``.
- See https://developer.hashicorp.com/terraform/cloud-docs/api-docs/variables#update-variables




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
                </td>
                <td>
                        <div>Terraform cloud API (HCP Terraform) url.</div>
                        <div>You should not change the value unless for test purpose.</div>
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
                    <b>variable_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The ID of the variable to update.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: id</div>
                </td>
            </tr>
    </table>
    <br/>



See Also
--------

.. seealso::

   :ref:`pytoccaz.terraform_cloud.tfc_workspace_var_update_module`
      The official documentation on the **pytoccaz.terraform_cloud.tfc_workspace_var_update** module.


Examples
--------

.. code-block:: yaml

    - name: Change the value of a variable with payload option
      tfc_var_update:
        variable_id: "var-sQaLVxPGd8Bhui56"
        token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
        payload:
          data:
            attributes:
              value: "var10"

    - name: Change the value of a variable with data option
      tfc_var_update:
        variable_id: "var-sQaLVxPGd8Bhui56"
        token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
        data:
          attributes:
            value: "var10"

    - name: Change the value of a variable with attributes option
      tfc_var_update:
        variable_id: "var-sQaLVxPGd8Bhui56"
        token: "{{ lookup('ansible.builtin.env', 'TERRA_TOKEN') }}"
        attributes:
          value: "var10"



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
                            <div>The data attribute from HCP Terraform route <code>PATCH /vars/:variable_id</code></div>
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
