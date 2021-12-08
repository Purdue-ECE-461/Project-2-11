# pip install --upgrade google-cloud-storage
# for some reason, my pip install isn't working, I don't know why, try this on your computer

import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'server/service.json'
storage_client = storage.Client()
instance_name = "ece461proj2trustmoduleregistry:us-east1:package-info"
'''
Creating a new bucket
'''

bucket_name = 'ece461proj2some'
# bucket = storage_client.bucket(bucket_name)
# bucket = storage_client.create_bucket(bucket,location = 'US')

'''
Printing bucket details
'''

# vars(bucket)

'''
Accessing a bucket
'''

my_bucket = storage_client.get_bucket(bucket_name)

'''
Uploading files
blob_name: name of file in gcs
file_path: of uploaded file
bucket_name: to upload to
'''


def uploadFiles(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False


file_path = r'/Users/dhruvavish/Documents/ECE461/Project-2-11/project-1'
uploadFiles('file1Name', os.path.join(file_path, r'kitten.png'), bucket_name)

'''
Downloading from bucket
'''


def downloadFiles(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path, "wb") as f:
            storage_client.download_blob_to_file(blob, f)

        return True
    except Exception as e:
        print(e)
        return False


def connect():
    socket = f'/cloudsql/{instance_name}'
    connection = pymsql.connect(user='root', password='2pjHC9svdbauJxFw', unix_socket=socket, db='package-info')
    return connection
