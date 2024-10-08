#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This is my test module for creation file by given path and content 

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    path:
        description: This is the where file will be created.
        required: true
        type: str
    content:
        description:
            - This is a content of the created file.
        required: false
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Sergey Nikiforov (@SeNike)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_own_module:
    path: ~/new_ansible.txt

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_own_module:
    path: '~/new_ansible.txt'
    content: 'Hello!'

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_own_module:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: '"changed": false, "failed": false, "original_message": "~/new_ansible.txt", "message": "~/new_ansible.txt,Hello!", "invocation": {"module_args": {"path": "~/new_ansible.txt", "content": "Hello"}}'
'''
import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        failed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True

    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    if not module.params['path']:
        module.params['path'] = '~/default.name'
    result['original_message'] = module.params['path']
    result['message'] = '{},{}!'.format(module.params['path'], module.params['content'])

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    #if module.params['new']:
    #    result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['path'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    path = os.path.expanduser(module.params['path'])
    content = module.params['content']

    # Try to create a file if it doesn't exists
    if not os.path.exists(path): 
        try:
            with open(path, 'w') as file:
                file.write(content)
            result = {'changed': True, 'msg': f'File {path} with content "{content}" created successfully'}
        except Exception as e:
            module.fail_json(msg=f"Failed to create file: {str(e)}")
    else:
        result = {'changed': False, 'msg': f'File {path} already exists'}


    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
