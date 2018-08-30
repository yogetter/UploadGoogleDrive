#!/bin/python
from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime, timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

"""Shows basic usage of the Drive v3 API.
Prints the names and ids of the first 10 files the user has access to.
"""
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

## list & Search File
# page_token = None
# while True:
#    results = service.files().list(pageSize=10, q="name contains 'conflu'", pageToken=page_token).execute()
#    items = results.get('files', [])
#
#    if not items:
#        print('No files found.')
#    else:
#        print('Files:')
#        for item in items:
#            print(item['name'], item['id'])
#    
#    page_token = results.get('nextPageToken', None)
#    if page_token is None:
#      break
#upload file
date = (datetime.now() - timedelta(1)).strftime("%Y_%m_%d")
folder_id = '1GmugVD69q9Q2e2pvCUNeNVbxKGx0NPuq'
file_metadata = {
    'name': 'backup-'+ date + '.zip',
    'parents': [folder_id] 
}
media = MediaFileUpload('/var/atlassian/application-data/confluence/backups/backup-'+ date + '.zip',
                        mimetype='application/zip',
                        resumable=True)
tmp_file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
print ('Upload File')
print ('Success: ID', tmp_file.get('id'))
