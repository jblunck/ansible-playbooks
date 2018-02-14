Ansible Dynamic Inventory Script for MAAS
=========================================

Requirements
------------
```
$ pip2 install requests requests_oauthlib
```

Configuration
-------------
This script assumes an `maas.ini` file in the same path as the script. A different
path can be defined by the `MAAS_INI_PATH` environment variable.

```
[DEFAULT]
# Explicitly set active profile (default: first profile section found).
# Overridden by environment variable MAAS_PROFILE.
#profile = prod

[test]
maas_server = 1.2.3.4
maas_api_key = <consumer_key>:<token>:<secret>

[prod]
maas_server = 5.6.7.8
maas_api_key = <consumer_key>:<token>:<secret>
```

> **Note:** A user's API key can be obtained from the web interface. Click on
> 'username' in the top right corner, and select 'Account'.

Usage Examples
--------------
```
$ ansible -i maas.py all --list-hosts
hosts (3):
  rapid-condor.maas
  test1.maas
  rich-tuna.maas
```

```
$ ansible-playbook -i maas.py debug-inventory.yml

PLAY [all] *********************************************************************

TASK [Display all variables/facts known for a host] ****************************
ok: [rapid-condor.maas] => {
    "hostvars[inventory_hostname]": {
        "ansible_check_mode": false,
        "ansible_playbook_python": "/usr/local/Cellar/ansible/2.4.2.0_2/libexec/bin/python",
        "ansible_ssh_host": "10.1.72.7",
        "ansible_ssh_user": "centos",
        "ansible_version": {
            "full": "2.4.2.0",
            "major": 2,
            "minor": 4,
            "revision": 2,
            "string": "2.4.2.0"
        },
        "group_names": [
            "maas_machines",
            "maas_status_deployed",
            "maas_tag_names_virtserver",
            "maas_zone_default"
        ],
        "groups": {
            "all": [
                "rapid-condor.maas",
                "test1.maas",
                "rich-tuna.maas"
            ],
            "maas_machines": [
                "rapid-condor.maas",
                "test1.maas",
                "rich-tuna.maas"
            ],
            "maas_status_deployed": [
                "rapid-condor.maas"
            ],
            "maas_status_failed_commissioning": [
                "rich-tuna.maas"
            ],
	    "maas_status_ready": [
                "test1.maas"
            ],
            "maas_tag_names_virtserver": [
                "rapid-condor.maas"
            ],
            "maas_tag_names_virtual": [
                "test1.maas",
                "rich-tuna.maas"
            ],
            "maas_zone_default": [
                "rapid-condor.maas",
                "test1.maas",
                "rich-tuna.maas"
            ],
            "ungrouped": []
        },
        "inventory_dir": "/Users/jblunck/GIT/ansible-playbooks/python-maas-inventory",
        "inventory_file": "/Users/jblunck/GIT/ansible-playbooks/python-maas-inventory/maas.py",
        "inventory_hostname": "rapid-condor.maas",
        "inventory_hostname_short": "rapid-condor",
        "maas_architecture": "amd64/generic",
        "maas_boot_interface": "50:9a:4c:57:f0:83",
        "maas_ip_addresses": [
            "10.1.72.7"
        ],
        "maas_mac_addresses": [
            "50:9a:4c:57:f0:83"
        ],
        "maas_owner": "admin",
        "maas_owner_data": {},
        "maas_system_id": "ywyehh",
        "omit": "__omit_place_holder__edf6f52270c879f7dbaf65823339c2065d769479",
        "playbook_dir": "/Users/jblunck/GIT/ansible-playbooks/python-maas-inventory"
    }
}
ok: [test1.maas] => {
    "hostvars[inventory_hostname]": {
        "ansible_check_mode": false,
        "ansible_playbook_python": "/usr/local/Cellar/ansible/2.4.2.0_2/libexec/bin/python",
        "ansible_version": {
            "full": "2.4.2.0",
            "major": 2,
            "minor": 4,
            "revision": 2,
            "string": "2.4.2.0"
        },
        "group_names": [
            "maas_machines",
            "maas_status_ready",
            "maas_tag_names_virtual",
            "maas_zone_default"
        ],
        "groups": {
            "all": [
                "rapid-condor.maas",
                "test1.maas",
                "rich-tuna.maas"
            ],
            "maas_machines": [
                "rapid-condor.maas",
                "test1.maas",
                "rich-tuna.maas"
            ],
            "maas_status_deployed": [
                "rapid-condor.maas"
            ],
            "maas_status_failed_commissioning": [
                "rich-tuna.maas"
            ],
            "maas_status_ready": [
                "test1.maas"
            ],
            "maas_tag_names_virtserver": [
                "rapid-condor.maas"
            ],
            "maas_tag_names_virtual": [
                "test1.maas",
                "rich-tuna.maas"
            ],
            "maas_zone_default": [
                "rapid-condor.maas",
                "test1.maas",
                "rich-tuna.maas"
            ],
            "ungrouped": []
        },
        "inventory_dir": "/Users/jblunck/GIT/ansible-playbooks/python-maas-inventory",
        "inventory_file": "/Users/jblunck/GIT/ansible-playbooks/python-maas-inventory/maas.py",
        "inventory_hostname": "test1.maas",
        "inventory_hostname_short": "test1",
        "maas_architecture": "amd64/generic",
        "maas_boot_interface": "52:54:00:05:be:96",
        "maas_ip_addresses": [],
	"maas_mac_addresses": [
            "52:54:00:05:be:96"
        ],
        "maas_owner": null,
        "maas_owner_data": {},
        "maas_system_id": "se678e",
        "omit": "__omit_place_holder__edf6f52270c879f7dbaf65823339c2065d769479",
        "playbook_dir": "/Users/jblunck/GIT/ansible-playbooks/python-maas-inventory"
    }
}
ok: [rich-tuna.maas] => {
    "hostvars[inventory_hostname]": {
        "ansible_check_mode": false,
        "ansible_playbook_python": "/usr/local/Cellar/ansible/2.4.2.0_2/libexec/bin/python",
        "ansible_version": {
            "full": "2.4.2.0",
            "major": 2,
            "minor": 4,
            "revision": 2,
            "string": "2.4.2.0"
        },
        "group_names": [
            "maas_machines",
            "maas_status_failed_commissioning",
            "maas_tag_names_virtual",
            "maas_zone_default"
        ],
        "groups": {
            "all": [
                "rapid-condor.maas",
                "test1.maas",
                "rich-tuna.maas"
            ],
            "maas_machines": [
                "rapid-condor.maas",
                "test1.maas",
                "rich-tuna.maas"
            ],
            "maas_status_deployed": [
                "rapid-condor.maas"
            ],
            "maas_status_failed_commissioning": [
                "rich-tuna.maas"
            ],
            "maas_status_ready": [
                "test1.maas"
            ],
            "maas_tag_names_virtserver": [
                "rapid-condor.maas"
            ],
            "maas_tag_names_virtual": [
                "test1.maas",
                "rich-tuna.maas"
            ],
            "maas_zone_default": [
                "rapid-condor.maas",
                "test1.maas",
                "rich-tuna.maas"
            ],
            "ungrouped": []
        },
        "inventory_dir": "/Users/jblunck/GIT/ansible-playbooks/python-maas-inventory",
        "inventory_file": "/Users/jblunck/GIT/ansible-playbooks/python-maas-inventory/maas.py",
        "inventory_hostname": "rich-tuna.maas",
        "inventory_hostname_short": "rich-tuna",
        "maas_architecture": "amd64/generic",
        "maas_ip_addresses": [],
	"maas_mac_addresses": [],
        "maas_owner": "admin",
        "maas_owner_data": {},
        "maas_system_id": "wgd4ra",
        "omit": "__omit_place_holder__edf6f52270c879f7dbaf65823339c2065d769479",
        "playbook_dir": "/Users/jblunck/GIT/ansible-playbooks/python-maas-inventory"
    }
}

PLAY RECAP *********************************************************************
rapid-condor.maas          : ok=1    changed=0    unreachable=0    failed=0
rich-tuna.maas             : ok=1    changed=0    unreachable=0    failed=0
test1.maas                 : ok=1    changed=0    unreachable=0    failed=0
```
