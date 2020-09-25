# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START drive_quickstart]
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Users\\doyun\\Documents\\work\\googledrive\\python-samples\\drive\\quickstart\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)

    ## Call the Drive v3 API
    #results = service.files().list(
    #    pageSize=100, fields="nextPageToken, files(id, name)").execute()
    #items = results.get('files', [])
#
    #if not items:
    #    print('No files found.')
    #else:
    #    print('Files:')
    #    for item in items:
    #        print(u'{0} ({1})'.format(item['name'], item['id']))


#video/mp4

#    page_token = None
#    while True: 
#        response = service.files().list(pageSize=100, q="mimeType='application/vnd.google-apps.folder' and '1ff4HfAvIhVG_vx5Z_OTdcSSG4reOI1yW' in parents", corpora='drive', driveId='0ALYTh_PzL_chUk9PVA', spaces='drive', supportsAllDrives=True, includeItemsFromAllDrives=True, fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
#        for file in response.get('files', []):
#            # Process change
#            print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
#        page_token = response.get('nextPageToken', None)
#        if page_token is None:
#            break

#UPLOAD
    file_metadata = {'name': 'temp.mp4', 'parents': ['1_SMN59B0HXxo7OHG2ETi7AzcpVl9Xv2L']}
    media = MediaFileUpload('F:\\temp.mp4', mimetype='video/mp4')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()
    print ('File ID: %s' % file.get('id'))

if __name__ == '__main__':
    main()
# [END drive_quickstart]


# SELECT A.ID, A.LOGIN, B.REGION, C.WORK, C.BROADCASTING, C.NOWTIME FROM tdb.STREAMERSTATUSLOG a , tdb.STREAMERS b, (SELECT ID, WORK, BROADCASTING, NOWTIME FROM (SELECT ID, WORK, BROADCASTING, NOWTIME, (ROW_NUMBER() OVER(PARTITION BY ID ORDER BY NOWTIME DESC)) RANK FROM TDB.STATUS WHERE NOWTIME > sysdate - 30) WHERE RANK = 1) c WHERE A.LOGIN = B.LOGIN and C.ID = A.ID and REGION='R420';