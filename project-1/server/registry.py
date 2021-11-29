from flask import Flask, redirect,url_for, request

app = Flask(__name__)


@app.route('/packages/',defaults = {'offset' : 1})
@app.route('/packages/<int:offset>',methods = ['GET'])
def getPackages(offset):
    return {"response":[offset]}

@app.route('/reset', methods = ['DELETE'])
def registryReset():
    return 'Uploading to Google Cloud Bucket'

@app.route('/package/<id>', methods = ['DELETE'])
def deletePackage(id):
    #Delete from package id
    return f'Deleting package {id}'

@app.route('/package/<id>', methods = ['PUT'])
def updatePackage(id):
    return f'Updating package {id}'

@app.route('/package/<id>', methods = ['GET'])
def packageRetrieve(id):
    return f'Retrieving package {id}'

@app.route('/package', methods = ['POST'])
def packageCreate():
    return 'Creating package'

@app.route('/authenticate', methods = ['PUT'])
def createAuthToken():
    return 'Creating Auth Token'

@app.route('/package/byName/<name>', methods = ['GET'])
def getPackageByName(name):
    return f'Retrieving package {name}'

@app.route('/package/byName/<name>', methods = ['DELETE'])
def deletePackageByName(name):
    return f'Deleting package {name}'

@app.route('/package/<id>/rate', methods = ['POST'])
def rate(id):
    return f'Rating Package {id}'




if __name__ == "__main__":
    app.run()