from flask import Flask, render_template,redirect,url_for, request
#from storage import uploadFiles,downloadFiles



app = Flask(__name__)


@app.route('/packages/',defaults = {'offset' : 1})
@app.route('/packages/<int:offset>',methods = ['GET']) #essential
def getPackages(offset):

    return {"response":[offset]}

@app.route('/reset', methods = ['DELETE'])
def registryReset():
    return 'Uploading to Google Cloud Bucket'

@app.route('/package/<id>', methods = ['DELETE']) #essential
def deletePackage(id):
    #Delete from package id
    return f'Deleting package {id}'

@app.route('/package/<id>', methods = ['PUT']) 
def updatePackage(id):
    return f'Updating package {id}'

@app.route('/package/<id>', methods = ['GET'])
def packageRetrieve(id):
    return f'Retrieving package {id}'

@app.route('/package', methods = ['POST']) #essential
def packageCreate():
    res = request.get_json()
    if not res:
        return 'No JSON object found', 400;
    return res
    #return 'Creating package'

@app.route('/authenticate', methods = ['PUT']) #essential
def createAuthToken():
    return 'Creating Auth Token'

@app.route('/package/byName/<name>', methods = ['GET'])
def getPackageByName(name):
    """
    select * from database where packageName == Name
    """
    return f'Retrieving package {name}' #essential


@app.route('/package/byName/<name>', methods = ['DELETE'])
def deletePackageByName(name): #essential
    return f'Deleting package {name}'

@app.route('/package/<id>/rate', methods = ['POST']) #essential
def rate(id):
    connection = connect()

    with connection.cursor() as cursor:
        cursor.execute(("select * from package"))

        frame = pd.DataFrame(cursor.fetchall())
        print(frame.head)

    """
    Get url
    run through project 1,
    get the scores
    """
    return 'Rating Package {id}'



@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
    rate(1)