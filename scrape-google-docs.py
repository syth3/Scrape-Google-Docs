from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly',
          'https://www.googleapis.com/auth/docs',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1cGCbZ8j1KPitO5SSsS6rAFMNWffDsgixH7mDQh6ZDu8'


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


def get_comments(document):
    # Get the document


    # comments = []
    #
    # # Get all the comments
    # for comment in doc['comments']:
    #     comment_text = comment['content']
    #     comments.append(comment_text)
    #
    # return comments
    pass


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    global DOCUMENT_ID

    creds = validate_creds()

    # service = build('docs', 'v1', credentials=creds)
    # document = service.documents().get(documentId=DOCUMENT_ID).execute()

    all_comments = []

    drive = build('drive','v3', credentials=creds)
    comments = drive.comments().list(fileId=DOCUMENT_ID, fields='comments,nextPageToken').execute()

    next_page_token = comments.get('nextPageToken')

    while next_page_token:
        for comment in comments.get('comments'):
            if not comment["resolved"]:
                all_comments.append(comment)
        comments = drive.comments().list(fileId=DOCUMENT_ID, pageToken=next_page_token,
                                         fields='comments,nextPageToken').execute()
        next_page_token = comments.get('nextPageToken')

    print()
    # try:
    #
    #
    #     # Retrieve the documents contents from the Docs service.
    #
    #
    #     print('The title of the document is: {}'.format(document.get('title')))
    # except HttpError as err:
    #     print(err)


if __name__ == '__main__':
    main()
