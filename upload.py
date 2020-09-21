from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from time import sleep

class upload():
    def __init__(self, storage):
        self.storage = storage
        self.uploadqueue = []
        SCOPES = ['https://www.googleapis.com/auth/drive']

        creds = None
        if os.path.exists('token.pickle'): with open('token.pickle', 'rb') as token: creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('config.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token: pickle.dump(creds, token)

        drive_service = build('drive', 'v3', credentials=creds)
    
    def main(self):
        while True:
            if self.uploadqueue == []: sleep(10)
            else:

                #Upload start
    
    def upload(self, parent):
        file_metadata = {'name': self.uploadqueue[0], 'parents': ['1_SMN59B0HXxo7OHG2ETi7AzcpVl9Xv2L']}
        media = MediaFileUpload(self.uploadqueue[0], mimetype='video/mp4')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()
        #print ('File ID: %s' % file.get('id'))
        self.uploadqueue.remove(self.uploadqueue[0])
