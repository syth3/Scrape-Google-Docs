from __future__ import print_function

import os.path
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly',
          'https://www.googleapis.com/auth/docs',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.readonly']

# The ID of a sample document.
DOCUMENT_ID = sys.argv[1]


def validate_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds-dontpush.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def pull_comments(creds):
    drive = build('drive', 'v3', credentials=creds)
    comments = drive.comments().list(fileId=DOCUMENT_ID, fields='comments,nextPageToken').execute()

    next_page_token = comments.get('nextPageToken')

    all_comments = []

    while next_page_token:
        for comment in comments.get('comments'):
            if not comment["resolved"]:
                all_comments.append(comment)
        comments = drive.comments().list(fileId=DOCUMENT_ID, pageToken=next_page_token,
                                         fields='comments,nextPageToken').execute()
        next_page_token = comments.get('nextPageToken')

    return all_comments


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    global DOCUMENT_ID

    creds = validate_creds()

    all_comments = pull_comments(creds)

    found_comment = None
    for comment in all_comments:
        if comment["quotedFileContent"]["value"] == "PROLOGUE":
            found_comment = comment

    # service = build('docs', 'v1', credentials=creds)
    # document = service.documents().get(documentId=DOCUMENT_ID).execute()

    print()


if __name__ == '__main__':
    main()
