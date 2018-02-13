#!/usr/bin/env python2

'''
MAAS dynamic inventory script
=============================

Generates a dynamic inventory for Ansible by using the MAAS REST api.

This script assumes an maas.ini file in the same path as the script. A different
path can be defined by the MAAS_INI_PATH environment variable.

  #[DEFAULT]
  #profile = prod
  #
  #[test]
  #maas_server = 1.2.3.4
  #maas_api_key = aaa:bbb:ccc
  #
  #[prod]
  #maas_server = 5.6.7.8
  #maas_api_key = ddd:eee:fff

A different profile can de defined at runtime by setting the MAAS_PROFILE
environment variable:

$ MAAS_PROFILE=test ./maas.py --list
'''

import argparse
import requests
from requests_oauthlib import OAuth1
import os

try:
	import json
except ImportError:
	import simplejson as json

try:
	import configparser
except ImportError:
	import ConfigParser as configparser

DEFAULTS = {
	'maas_server': 'localhost',
	'maas_api_key': '::'
}

def perform_API_request(server, path, api_key):
	keys = api_key.split(':')

	authheader = OAuth1(keys[0], None, keys[1], keys[2],
		signature_type='auth_header', signature_method='PLAINTEXT')

	url = "http://%s/MAAS" % (server)
	url += path
	return requests.get(url, auth=authheader, headers={'Accept': 'application/json,*/*'})

def add_host(d, group, fqdn):
	if not d.has_key(group):
		d.update({ group:{ 'hosts':[], 'vars':{}} })
	d[group]['hosts'].append(fqdn)
	return d

def add_hostvars(d, fqdn, k, v):
	if not d.has_key('_meta') or not d['_meta'].has_key('hostvars'):
		d.update({ '_meta':{ 'hostvars':{ }} })
	if not d['_meta']['hostvars'].has_key(fqdn):
		d['_meta']['hostvars'].update({ fqdn:{ k: v } })
	else:
		d['_meta']['hostvars'][fqdn].update({ k: v })
	return d

class MaasInventory:

	def __init__(self):

		self.read_settings()

	def read_settings(self):
		defaults = {
			'ini_path': os.path.join(os.path.dirname(__file__), 'maas.ini')
		}

		self.config = configparser.ConfigParser(DEFAULTS)

		ini_path = os.environ.get('MAAS_INI_PATH', defaults['ini_path'])
		if os.path.isfile(ini_path):
			self.config.read(ini_path)

		# The profile to use:
		#  0. the default section
		self.profile = configparser.DEFAULTSECT

		#  1. the first non-default section of the ini
		if len(self.config.sections()) > 0:
			self.profile = self.config.sections()[0]

		#  2. the default sections 'profile' option
		if self.config.has_option(configparser.DEFAULTSECT, 'profile'):
			self.profile = self.config.get(configparser.DEFAULTSECT, 'profile')

		#  3. the environment variable MAAS_PROFILE
		self.profile = os.environ.get('MAAS_PROFILE', self.profile)

	def get_nodes(self):
		maas_server = os.environ.get('MAAS_SERVER',
			self.config.get(self.profile, 'maas_server'))
		maas_api_key = os.environ.get('MAAS_API_KEY',
			self.config.get(self.profile, 'maas_api_key'))
		keys = maas_api_key.split(':')

		# API key = '<consumer_key>:<token>:<secret>'
		r = perform_API_request(maas_server, '/api/2.0/nodes/', maas_api_key)
		return json.loads(r.text)

	def get_host(self, hostname):
		nodes = self.get_nodes()

		for n in nodes:
			if n['node_type'] != 0:
				continue

			if hostname != n['fqdn']:
				continue

			return n

		return {}

	def get_machines(self):
		nodes = self.get_nodes()
		machines = {}

		for n in nodes:
			if n['node_type'] != 0:
				continue

			host = n['fqdn']

			# all machines are in 'maas_machines'
			add_host(machines, 'maas_machines', host)

			# machines grouped by zone
			add_host(machines, 'maas_zone_' + n['zone']['name'], host)

			# machines grouped by tag names
			for tag in map(lambda x: 'maas_tag_names_' + x, n['tag_names']):
				add_host(machines, tag, host)

			# machines grouped by status
			add_host(machines, 'maas_status_' + n.get('status_name', 'Unknown'),
				host)

			#
			# add maas hostvars for all machines
			#
			add_hostvars(machines, host, 'maas_architecture', n['architecture'])
			add_hostvars(machines, host, 'maas_system_id', n['system_id'])
			add_hostvars(machines, host, 'maas_owner', n['owner'])
			add_hostvars(machines, host, 'maas_owner_data', n['owner_data'])

			add_hostvars(machines, host, 'maas_ip_addresses', n['ip_addresses'])

			# FIXME: mac address missing if machine isn't deployed
			if n['boot_interface']:
				add_hostvars(machines, host, 'maas_boot_interface', n['boot_interface']['mac_address'])

			mac_addresses = []
			for item in n.get('interface_set', []):
				mac_addresses.append(item['mac_address'])
			add_hostvars(machines, host, 'maas_mac_addresses', sorted(mac_addresses))

			#
			# add ansible hostvars for deployed machines
			#
			if n['status'] != 6:
				continue

			if len(n['ip_addresses']) > 0:
				add_hostvars(machines, host, 'ansible_ssh_host', n['ip_addresses'][0])

			add_hostvars(machines, host, 'ansible_ssh_user', n['osystem'])

		return machines

def args_parse():
    parser = argparse.ArgumentParser(description='Ansible MAAS inventory module')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true',
					   help='List active servers')
    group.add_argument('--host', help='List details about the specified host')

    return parser.parse_args()

def main():
	args = args_parse()
	result = {}

	if args.host:
		result = MaasInventory().get_host(args.host)
	elif args.list:
		result = MaasInventory().get_machines()

	print(json.dumps(result, indent=1))

if __name__ == '__main__':
	main()
