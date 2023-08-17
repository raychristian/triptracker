"""
Retrieve secrets from secrets manager
"""

import os

from google.cloud.secretmanager import SecretManagerServiceClient

def get(name):
	print(os.environ)

	""" Get value with given key """
	
	project = os.environ['GOOGLE_CLOUD_PROJECT']
	is_gae = os.environ['GAE_APPLICATION']
	
	if is_gae:
		client = SecretManagerServiceClient()
		secret_path = f'projects/{project}/secrets/{name}/versions/latest'

		res = client.access_secret_version(request={'name': secret_path})
		value = res.payload.data.decode('utf-8')

		return value

	return os.environ[name]
