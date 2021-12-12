# pip install --upgrade google-cloud-storage
# for some reason, my pip install isn't working, I don't know why, try this on your computer

import os
import base64
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'service.json'
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


def uploadFiles(blob_name, file_content):
    print(file_content)
    with open(blob_name, "wb") as f:
        f.write(file_content.encode('utf-8'))

    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(blob_name)
        os.remove(blob_name)
        return True
    except Exception as e:
        print(e)
        return False


'''
Downloading from bucket
'''


def downloadFiles(blob_name):

    print(blob_name)

    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(blob_name+".zip", "wb") as fin:
            storage_client.download_blob_to_file(blob, fin)
        with open(blob_name+".zip", "rb") as fin:
            str = fin.read()
        with open(blob_name+".zip", "wb") as fout:
            fout.write(base64.b64decode(str))
            
            

        
        return blob_name+".zip"
    except Exception as e:
        print(e)
        return False

# if __name__ == "__main__":
#     with open('proj1_3.zip', 'rb') as fin, open('pro.zip.b64', 'wb') as fout:
#         base64.encode(fin, fout)
#     fp = open("output.zip.b64", "rb")
#     bytes = fp.read()
#     uploadFiles("proj1_3", base64.b64encode(bytes))

