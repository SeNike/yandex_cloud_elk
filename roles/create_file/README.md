### Role: create_file

The create_file role utilizes the my_own_module to create a text file with specified content.

## Requirements

This role requires Ansible 2.9 or higher.

## Variables

This role accepts the following variables:    

| Variable | Type   | Required | Description                                  |
|-----------|--------|----------|----------------------------------------------|
| file_path    | string | Yes      | The path where the text file will be created (e.g., `/home/user/test.txt`). Use `~` for the home directory. |
| file_content | string | Yes      | The content to write into the text file.    |

Role Name
=========

The create_file role utilizes the my_own_module to create a text file with specified content.

Requirements
------------

This role requires Ansible 2.9 or higher.

Role Variables
--------------

This role accepts the following variables:    

| Variable | Type   | Required | Description                                  |
|-----------|--------|----------|----------------------------------------------|
| file_path    | string | Yes      | The path where the text file will be created (e.g., `/home/user/test.txt`). Use `~` for the home directory. |
| file_content | string | Yes      | The content to write into the text file.    |


Example Playbook
----------------

``` yaml
---
- name: Run create_file role
  hosts: localhost
  vars:
    file_path: '~/test_ansible_new.txt'
    file_content: 'Test passed'
  roles:
    - role: create_file
```

License
-------

MIT

Author Information
------------------

Sergey Nikiforov
