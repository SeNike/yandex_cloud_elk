# Ansible Collection - senike.yandex_cloud_elk

# My Ansible Collection

## Overview

This Ansible collection provides a custom module `my_own_module` for creating text files on remote hosts and a role `create_file` that utilizes this module to manage file creation.

## Contents

- **Module: `my_own_module`**
- **Role: `create_file`**

## Module: `my_own_module`

The `my_own_module` is a custom Ansible module that creates a text file on a remote host with specified content.

### Parameters

| Parameter | Type   | Required | Description                                  |
|-----------|--------|----------|----------------------------------------------|
| `path`    | string | Yes      | The path where the text file will be created (e.g., `/home/user/test.txt`). Use `~` for the home directory. |
| `content` | string | Yes      | The content to write into the text file.    |

### Example Usage

```yaml
- name: Create a text file using my_own_module
  my_own_module:
    path: "~/test_file.txt"
    content: "Hello, World!"
```    

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

## Example Playbook

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

### License
This collection is licensed under the MIT License. See the LICENSE file for details.

### Author

Sergey Nikiforov