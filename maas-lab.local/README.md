# Ansible Playbook: MAAS

This playbook helps with managing your MAAS infrastructure. It makes use of the
[mrlesmithjr.maas][1] role but the dynamic inventory playbook is heavily
inspired by the [Ansible - MAAS Management blog posting][0].

## Playbook Variables



## Dependencies

See `requirements.yml`.

## Example Usage

Retrieve an MAAS CLI api key from your MAAS server instance at
http://your-maas.server/MAAS/account/prefs/ and place it a new vault file:
```
$ ansible-vault create files/maas-secrets.yml
maas_login_user: 'admin'
maas_login_apikey: 'aaaaaaaaaaaaaaaaaa:bbbbbbbbbbbbbbbbbb:ccccccccccccccccdddddddddddddddd'
```

After that run the inventory playbook to see the dynamic inventory contents:

```
$ ansible-playbook -i staging -e@files/maas-secrets.yml maas-inventory.yml --tags debug

.
.
.

TASK [DEBUG - list of maas_machines] ***************************************************************************
ok: [meet-ant.maas] => (item=test2.maas) => {
    "changed": false,
    "item": "test2.maas",
    "msg": "test2.maas"
}
ok: [maas.maas] => (item=test2.maas) => {
    "changed": false,
    "item": "test2.maas",
    "msg": "test2.maas"
}
ok: [test2.maas] => (item=test2.maas) => {
    "changed": false,
    "item": "test2.maas",
    "msg": "test2.maas"
}
ok: [meet-ant.maas] => (item=meet-ant.maas) => {
    "changed": false,
    "item": "meet-ant.maas",
    "msg": "meet-ant.maas"
}
ok: [maas.maas] => (item=meet-ant.maas) => {
    "changed": false,
    "item": "meet-ant.maas",
    "msg": "meet-ant.maas"
}
ok: [test2.maas] => (item=meet-ant.maas) => {
    "changed": false,
    "item": "meet-ant.maas",
    "msg": "meet-ant.maas"
}

TASK [debug] ***************************************************************************************************
ok: [meet-ant.maas] => {
    "msg": [
        "maas_machines",
        "maas_virtserver",
        "virtserver"
    ]
}
ok: [maas.maas] => {
    "msg": [
        "maas"
    ]
}
ok: [test2.maas] => {
    "msg": [
        "maas_machines",
        "maas_virtual"
    ]
}

PLAY RECAP *****************************************************************************************************
maas.maas                  : ok=8    changed=0    unreachable=0    failed=0
meet-ant.maas              : ok=3    changed=0    unreachable=0    failed=0
test2.maas                 : ok=3    changed=0    unreachable=0    failed=0
```

The MAAS machines are added to dynamic groups based on the tags that have been
assigned to them. The example shows how the tag *virtual* which is automatically
added to virtual machines are in the *maas_virtual* group.

To statically reference the dynamic groups in your inventory files you need to
predefine them as empty static groups (also see the [official documentation][2]):
```
[maas_virtual]
# Dynamic group for MAAS managed machines

[virtual:children]
maas_virtual
```

## License

BSD

## Author Information

Jan Blunck
* jblunck at infradead.org

[0]: https://everythingshouldbevirtual.com/automation/ansible-maas-management/
[1]: https://github.com/mrlesmithjr/ansible-maas
[2]: http://docs.ansible.com/ansible/latest/intro_dynamic_inventory.html#static-groups-of-dynamic-groups
