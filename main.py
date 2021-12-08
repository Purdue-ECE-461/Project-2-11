from flask import Flask, render_template,redirect,url_for, request
from storage import uploadFiles,downloadFiles
from sqlconnector import connect
import pandas as pd
import json


app = Flask(__name__)
cnx = connect()
if not cnx:
    exit("Error connecting to database")

@app.route('/packages/',defaults = {'offset' : 1})
@app.route('/packages/<int:offset>',methods = ['GET']) #essential
def getPackages(offset):
    cursor = cnx.cursor(buffered = True)
    query = "SELECT * FROM package ORDER BY id LIMIT %s,10;"
    cursor.execute(query,((offset-1)*10 if offset > 0 else 0,))
    resp = pd.DataFrame(cursor.fetchall())
    cnx.commit()
    resp.columns = cursor.column_names
    resp = resp.to_json(orient='records')
    cursor.close()
    return resp

@app.route('/reset', methods = ['DELETE'])
def registryReset():
    cursor = cnx.cursor(buffered = True)
    query = "DELETE FROM package;"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    return 'Reset Registry'

@app.route('/package/<id>', methods = ['DELETE']) #essential
def deletePackage(id):
    #Delete from package id
    cursor = cnx.cursor(buffered = True)
    cursor.execute("DELETE FROM package WHERE id = %s",(id,))
    cursor.execute("SELECT ROW_COUNT()")
    cnx.commit()
    if cursor.fetchone()[0] == 0:
        return 'Package not found', 400
    return 'Package Deleted',200

@app.route('/package/<id>', methods = ['PUT']) 
def updatePackage(id):
    #Update package
    cursor = cnx.cursor(buffered = True)
    cursor.execute("SELECT * FROM package WHERE id = %s",(id,))
    if cursor.rowcount == 0:
        return 'Package not found', 400
    data = request.get_json()
    query = "UPDATE package SET package_name = %s, version = %s, url = %s,  WHERE id = %s;"
    cursor.execute(query,(data['metadata']['Name'],data['metadata']['Version'],data['data']['URL'],id))
    cnx.commit()
    return f'Updated package {id}',200

@app.route('/package/<id>', methods = ['GET'])
def packageRetrieve(id):
    cursor = cnx.cursor(buffered = True)
    cursor.execute("SELECT * FROM package WHERE id = %s",(id,))
    packageData = pd.DataFrame(cursor.fetchall())
    if packageData.empty:
        return 'Package not found', 400
    packageData.columns = cursor.column_names
    print(packageData)
    resp = packageData.to_json(orient='records')
    resp = resp[1:-1] #remove first and last element
    resp = "{" + resp + "}"
    print(resp,type(resp))
    return resp, 200

@app.route('/package', methods = ['POST']) #essential
def packageCreate():
    ''' upload file to gcp storage bucket'''
    req = request.get_json()
    if not (req and req['metadata']['Name'] and req['metadata']['Version']):
        return 'Invalid Request', 400
    cursor = cnx.cursor(buffered = True)
    #Check if package exists
    cursor.execute("SELECT * FROM package WHERE package_name = %s AND version = %s",(req['metadata']['Name'],req['metadata']['Version']))
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO package (id, package_name, version, url, content, jsprogram) VALUES (id, %s,%s,%s,%s,%s)""",
                (req['metadata']['Name'] , req['metadata']['Version'] , req['data']['URL'] , req['data']['Content'] , req['data']['JSProgram']))
        cnx.commit()
        cursor.execute("SELECT * FROM package WHERE package_name = %s AND version = %s",(req['metadata']['Name'],req['metadata']['Version']))
        resp = pd.DataFrame(cursor.fetchall())
        resp.columns = cursor.column_names
        resp = resp.to_json(orient='records')
        return resp[1:-1], 201
    else:
        cursor.close()
        return "Package already exists", 403
    #return 'Creating package'

@app.route('/authenticate', methods = ['PUT']) #essential
def createAuthToken():
    return 'Creating Auth Token'

@app.route('/package/byName/<name>', methods = ['GET'])
def getPackageByName(name):
    """
    select * from database where packageName == Name
    """
    cursor = cnx.cursor(buffered = True)
    cursor.execute("SELECT * FROM package WHERE package_name = %s",(name,))
    packageData = pd.DataFrame(cursor.fetchall())
    if packageData.empty:
        return 'Package not found', 400
    packageData.columns = cursor.column_names
    print(packageData)
    resp = packageData.to_json(orient='records')
    resp = resp[1:-1] #remove first and last element 
    resp = "{" + resp + "}"
    print(resp,type(resp))
    return resp, 200


@app.route('/package/byName/<name>', methods = ['DELETE'])
def deletePackageByName(name): #essential
    cursor = cnx.cursor(buffered = True)
    cursor.execute("DELETE FROM package WHERE package_name = %s",(name,))
    cursor.execute("SELECT ROW_COUNT()")
    cnx.commit()
    if cursor.fetchone()[0] == 0:
        return 'Package not found', 400
    return 'Package Deleted',200

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