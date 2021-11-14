from flask import Flask

app = Flask(__name__)


@app.route('/download',methods = ['GET'])
def download():
    return 'Downloading from Google Cloud Bucket'

@app.route('/upload', methods = ['POST'])
def upload():
    return 'Uploading to Google Cloud Bucket'

@app.route('/rate/<package_name>', methods = ['POST'])
def rate():
    return 'Rate Package'




if __name__ == "__main__":
    app.run()