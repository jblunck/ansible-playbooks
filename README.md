# Requirements

ansible-galaxy install --roles-path roles -r requirements.yml

# Vault

ERROR! Attempting to decrypt but no vault secrets found

export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault_password

# Run playbook

ansible-playbook -i staging site.yml

