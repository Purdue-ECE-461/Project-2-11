import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "gcpKeys/ece461proj2trustmoduleregistry-4753c1f12dad.json"
storage_client = storage.Client()


'''
Creating a new bucket
'''

bucket_name = 'data_bucket'
bucket = storage_client.bucket(bucket_name)
bucket.location = 'US'
bucket = storage_client.create_bucket(bucket)

'''
Printing bucket details
'''

vars(bucket)

'''
Accessing a bucket
'''

my_bucket = storage_client.get_bucket('data_bucket')


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

file_path = r'C:\Users\...'
uploadFiles('file1Name', os.path.join(file_path, 'kitten.png'), 'data_bucket')

'''
Downloading from bucket
'''
# pip install --upgrade google-cloud-storage
# for some reason, my pip install isn't working, I don't know why, try this on your computer

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