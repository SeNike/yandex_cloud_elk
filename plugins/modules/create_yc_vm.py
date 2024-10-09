#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: create_yc_vm

short_description: This module create a VM in Yandex Cloud with given parameters 

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module create a VM in Yandex Cloud with given parameters

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
import subprocess
import json
import os
from ansible.module_utils.basic import AnsibleModule
import yaml
import time
import paramiko
from socket import timeout, error as socket_error


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        vm_subnet=dict(type='str', required=True),
        vm_network=dict(type='str', required=True),
        vm_name=dict(type='str', required=True),
        vm_image_family=dict(type='str', required=True),
        vm_zone=dict(type='str', required=True),
        vm_cores=dict(type='str', required=True),
        vm_memory=dict(type='str', required=True),
        vm_disk_size=dict(type='str', required=True),
        vm_ssh_key_path=dict(type='str', required=True),
        host_name=dict(type='str', required=True)
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
    #if not module.params['vm_name']:
    #    module.params['vm_name'] = 'default-vm'
    #result['original_message'] = module.params['vm_name']
    #result['message'] = '{},{}!'.format(module.params['vm_name'], module.params['vm_name'])

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    #if module.params['new']:
    #    result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    #if module.params['wm_name'] == 'fail me':
    #    module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    SUBNET_NAME = module.params['vm_subnet']
    NETWORK_NAME = module.params['vm_network']
    VM_NAME =  module.params['vm_name']
    VM_IMAGE_FAMILY = module.params['vm_image_family']
    ZONE =  module.params['vm_zone']
    VM_CORES =  module.params['vm_cores']
    VM_MEMORY = module.params['vm_memory']
    VM_DISK_SIZE =  module.params['vm_disk_size']
    SSH_KEY_PATH =  module.params['vm_ssh_key_path']
    INVENTORY_FILE = "./inventory/prod.yml"
    HOST_NAME = module.params['host_name']
    
    #SUBNET_NAME = "my-subnet"
    #NETWORK_NAME = "my-network"
    #VM_NAME = "my-vm2"
    #ZONE = "ru-central1-a"
    #VM_CORES = 2
    #VM_MEMORY = 4
    #VM_DISK_SIZE = 20
    #SSH_KEY_PATH = "~/.ssh/id_rsa.pub"
    


    # Try to create a file if it doesn't exists



    # Параметры для подсети и виртуальной машины

    def run_command(command, parse_json=True):
        """Запускает команду и возвращает JSON-парсинг вывода, если это указано."""
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if parse_json:
                # Пытаемся декодировать JSON, если это указано
                return json.loads(result.stdout)
            else:
                # Если не указано декодирование JSON, возвращаем текстовый результат
                print(result.stdout)
                return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Ошибка выполнения команды '{command}': {e.stderr}")
            return None
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON из команды '{command}': {result.stdout}")
            return None

    def subnet_exists(subnet_name):
        """Проверяет существование подсети."""
        subnets = run_command("yc vpc subnet list --format json")
        return any(subnet['name'] == subnet_name for subnet in subnets) if subnets else False

    def create_subnet():
        """Создает новую подсеть."""
        print(f"Создание подсети {SUBNET_NAME}...")
        command = (
            f"yc vpc network create --name {NETWORK_NAME} --description 'Custom network' && "
            f"yc vpc subnet create --name {SUBNET_NAME} --zone {ZONE} --range 10.0.0.0/24 --network-name {NETWORK_NAME}"
        )
        run_command(command, parse_json=False)  # Ожидаем текстовый вывод
        result = {'changed': True, 'msg': f'Подсеть {SUBNET_NAME} создана.'}
        print("Подсеть создана.")

    def vm_exists(vm_name):
        """Проверяет существование виртуальной машины."""
        vms = run_command("yc compute instance list --format json")
        return any(vm['name'] == vm_name for vm in vms) if vms else False

    def create_vm():
        """Создает виртуальную машину."""
        print(f"Создание виртуальной машины {VM_NAME}...")
        command = (
            f"yc compute instance create "
            f"--name {VM_NAME} "
            f"--zone {ZONE} "
            f"--network-interface subnet-name={SUBNET_NAME},nat-ip-version=ipv4 "
            f"--memory {VM_MEMORY} "
            f"--cores {VM_CORES} "
            f"--create-boot-disk image-folder-id=standard-images,image-family={VM_IMAGE_FAMILY},size={VM_DISK_SIZE} "
            f"--ssh-key {SSH_KEY_PATH}"
            #f"--metadata ssh_keys='centos:{ssh_key}"
        )
        vm_info = run_command(command, parse_json=False)  # Ожидаем текстовый вывод
        print("Виртуальная машина создана.")
        result = {'changed': True, 'msg': f'Виртуальная машина {VM_NAME} создана.'}
        return vm_info

    def get_vm_ip(vm_name):
        """Получает IP-адрес виртуальной машины."""
        vms = run_command("yc compute instance list --format json")
        for vm in vms:
            if vm['name'] == vm_name:
                return vm['network_interfaces'][0]['primary_v4_address']['one_to_one_nat']['address']
        return None

    def update_inventory(hostname, ip_address):
        """Обновляет или добавляет запись в inventory-файл в нужном формате."""
        # Загружаем текущий инвентарь или создаем пустой словарь, если файл не существует
        inventory = {}
        if os.path.exists(INVENTORY_FILE):
            with open(INVENTORY_FILE, 'r') as f:
                inventory = yaml.safe_load(f) or {}

        # Структура файла в формате YAML
        if f'{HOST_NAME}' not in inventory:
            inventory[f'{HOST_NAME}'] = {'hosts': {}}
        if 'hosts' not in inventory[f'{HOST_NAME}']:
            inventory[f'{HOST_NAME}']['hosts'] = {}

        # Добавляем или обновляем запись для указанного хоста
        inventory[f'{HOST_NAME}']['hosts'][hostname] = {
            'ansible_host': ip_address,
            'ansible_ssh_common_args': '-o StrictHostKeyChecking=no',
            'ansible_user': 'yc-user'
        }

        # Записываем изменения в файл, создавая папки при необходимости
        os.makedirs(os.path.dirname(INVENTORY_FILE), exist_ok=True)
        with open(INVENTORY_FILE, 'w') as f:
            yaml.dump(inventory, f)
        print(f"Инвентарь обновлен: {hostname} -> {ip_address}")


    def wait_for_ssh(hostname, username, ssh_key_path, timeout_sec=300, interval_sec=10):
        """Ожидает доступности SSH на указанном хосте в течение заданного таймаута."""
        end_time = time.time() + timeout_sec
        while time.time() < end_time:
            try:
                print(f"Проверка доступности SSH на {hostname}...")
                # Настройка SSH-клиента
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    hostname,
                    username=username,
                    key_filename=ssh_key_path,
                    timeout=10
                )
                print(f"Хост {hostname} доступен по SSH.")
                ssh.close()
                return True
            except (socket_error, timeout, paramiko.ssh_exception.NoValidConnectionsError):
                print(f"Хост {hostname} пока недоступен. Ожидание {interval_sec} секунд перед повторной проверкой.")
                time.sleep(interval_sec)

        print(f"Не удалось дождаться доступности SSH на {hostname} за {timeout_sec} секунд.")
        return False

    # Проверка и создание подсети при необходимости
    if not subnet_exists(SUBNET_NAME):
        create_subnet()
    else:
        print(f"Подсеть {SUBNET_NAME} уже существует.")
        result = {'changed': False, 'msg': f"Подсеть {SUBNET_NAME} уже существует."}

    # Проверка и создание виртуальной машины при необходимости
    if not vm_exists(VM_NAME):
        create_vm()
    else:
        print(f"Виртуальная машина {VM_NAME} уже существует.")
        result = {'changed': False, 'msg': f"Виртуальная машина {VM_NAME} уже существует."}

    # Получаем IP-адрес и обновляем inventory
    ip_address = get_vm_ip(VM_NAME)
    if ip_address:
        update_inventory(VM_NAME, ip_address)
    else:
        print("Не удалось получить IP-адрес для обновления инвентаря.")  

    wait_for_ssh(ip_address, 'yc-user', '/home/se/.ssh/id_rsa.pub', timeout_sec=300, interval_sec=10)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
