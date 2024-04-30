## v2.1.0 (2024-04-30)

- Change `hcp` prefix module name by `tfc` as it was at first. `hcp` prefix is a bad choice:
  - Rename `hcp_var_update` to `tfc_var_update`
  - Rename `hcp_workspace_info` to `tfc_workspace_info`
  - Rename `hcp_workspace_update` to `tfc_workspace_update`
  - Rename `hcp_workspace_var_update` to `tfc_workspace_var_update`
  - Rename `hcp_workspace_vars_info` to `tfc_workspace_vars_info`
  - Rename `hcp_workspaces_info` to `tfc_workspaces_info`
- Handle error when `requests` library is missing
- Pass sanity tests


## v2.0.0 (2024-04-26)

- Add `hcp_var_update` module
- Add `hcp_workspace_var_update` module
- Add `hcp_workspace_update` module
- Add `hcp_workspace_info` module
- Rename `tfc_workspaces_info` to `hcp_workspaces_info`
- Rename `tfc_workspace_vars_info` to `hcp_workspace_vars_info`
- Suppress version option from v1 modules

## v1.0.0 (2024-01-12)

- Add `tfc_workspaces_info` module
- Add `tfc_workspace_vars_info` module