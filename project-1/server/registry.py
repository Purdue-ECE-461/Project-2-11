from flask import Flask, redirect,url_for, request

app = Flask(__name__)


@app.route('/packages/<offset>',defaults = {'<offset>' : '<1>'},methods = ['GET'])
def getPackages():
    return {"response":[]}

@app.route('/reset', methods = ['DELETE'])
def registryReset():
    return 'Uploading to Google Cloud Bucket'

@app.route('/package/<id>', methods = ['DELETE'])
def deletePackage():
    #Delete from package id
    pass
@app.route('/package/<id>', methods = ['PUT'])
def updatePackage():
    pass
@app.route('/package/<id>', methods = ['GET'])
def packageRetrieve():
    pass

@app.route('/package', methods = ['POST'])
def packageCreate():
    pass

@app.route('/authenticate', methods = ['PUT'])
def createAuthToken():
    pass

@app.route('/package/byName/<name>', methods = ['GET'])
def getPackageByName():
    pass

@app.route('/package/byName/<name>', methods = ['DELETE'])
def deletePackageByName():
    pass

@app.route('/package/<id>/rate', methods = ['POST'])
def rate():
    return 'Rate Package'




if __name__ == "__main__":
    app.run()