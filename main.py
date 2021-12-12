from os import sendfile
from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory,make_response,jsonify,send_file
from flask_executor import Executor
from storage import uploadFiles,downloadFiles
from sqlconnector import connect
import base64
import pandas as pd
import jwt
import datetime
import json
from functools import wraps
from helper import *


PROPAGATE_EXCEPTIONS = True

app = Flask(__name__)
executor = Executor(app)
cnx = connect()
if not cnx:
    exit("Error connecting to database")
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['SECRET_KEY'] = 'testkey'
app.config['TESTSECRET'] = 'testkey'
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Authorization')

        if not token:
            return "Token is Missing"

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
        except Exception as e:
            print(e)
            return "Token Invalid"
        
        return f(*args, **kwargs)
    return decorated

@app.route('/authenticate', methods = ['PUT']) #essential
def createAuthToken():
    
    user_id = request.get_json()["User"]["name"]
    pwd = request.get_json()["Secret"]["password"]
    admin = request.get_json()["User"]["isAdmin"]

    auth = request.authorization

    if admin:
        print("aaaa")
        token = jwt.encode({'user' : user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'],'HS256').decode('utf-8')
        return jsonify({'token' : token})

    return "Authentication failed" , 401


@app.route('/packages/',defaults = {'offset' : 1})
@app.route('/packages/<int:offset>',methods = ['GET']) #essential
@token_required
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
@token_required
def registryReset():
    cursor = cnx.cursor(buffered = True)
    query = "DELETE FROM package;"
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    return 'Reset Registry'

@app.route('/package/<id>', methods = ['DELETE']) #essential
@token_required
def deletePackage(id):
    #Delete from package id
    cursor = cnx.cursor(buffered = True)
    cursor.execute("DELETE FROM package WHERE package_id = %s",(id,))
    cursor.execute("SELECT ROW_COUNT()")
    cnx.commit()
    if cursor.fetchone()[0] == 0:
        return 'Package not found', 400
    return 'Package Deleted',200

@app.route('/package/<id>', methods = ['PUT']) 
@token_required
def updatePackage(id):
    #Update package
    cursor = cnx.cursor(buffered = True)
    cursor.execute("SELECT * FROM package WHERE package_id = %s",(id,))
    if cursor.rowcount == 0:
        return 'Package not found', 400
    data = request.get_json()
    query = "UPDATE package SET package_name = %s, version = %s, url = %s, jsprogram = %s  WHERE package_id = %s;"
    cursor.execute(query,(data['metadata']['Name'],data['metadata']['Version'],data['data']['URL'],data['data']['JSProgram'],id))

    write_url(data['data']['URL'])
    run_scoring()
    with open("dict.txt") as fptr:
        dict_resp = json.loads(fptr.read())
    isIngest = ingestibilty(dict_resp)
    if (isIngest) is not True:
        cursor.close()
        return "Ingestibility failed. Package was not uploaded to database.", 403
    cnx.commit()
    query = "UPDATE package SET ramp_up = %s, correctness = %s, bus_factor = %s, responsiveness = %s, license = %s, dependancy = %s, overall = %s  WHERE package_id = %s;"
    cursor.execute(query,(dict_resp['ramp_up'],dict_resp['correctness'],dict_resp['bus_factor'],dict_resp['responsiveness'],dict_resp['license'],dict_resp['dependency'],dict_resp['score'], data['metadata']['ID']))#dict_resp['correctness'],dict_resp['bus_factor'],dict_resp['responsiveness'],dict_resp['license'],dict_resp['dependency'],dict_resp['score'],id))    
    cnx.commit()
    return 'Updated package ' + id,200

@app.route('/package/<id>', methods = ['GET'])
@token_required
def packageRetrieve(id):
    cursor = cnx.cursor(buffered = True)
    cursor.execute("SELECT * FROM package WHERE package_id = %s",(id,))
    packageData = pd.DataFrame(cursor.fetchall())
    if packageData.empty:
        return 'Package not found', 400
    packageData.columns = cursor.column_names
    resp = packageData.to_json(orient='records')
    resp = resp[1:-1] #remove first and last element
    resp = "{" + resp + "}"
    fname = downloadFiles(packageData['package_id'][0])
    return send_file(fname, as_attachment=True)

    return resp, 200



@app.route('/package', methods = ['POST']) #essential
@token_required
def packageCreate():
    ''' upload file to gcp storage bucket'''
    req = request.get_json()
    if not (req and req['metadata']['Name'] and req['metadata']['Version']):
        return 'Invalid Request', 400
    cursor = cnx.cursor(buffered = True)
    #Check if package exists
    cursor.execute("SELECT * FROM package WHERE package_id = %s",(req['metadata']['ID'],))

    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO package (id, package_id, package_name, version, url, jsprogram) VALUES (id,%s,%s,%s,%s,%s)""",
                (req['metadata']['ID'],req['metadata']['Name'] , req['metadata']['Version'] , req['data']['URL'] , req['data']['JSProgram']))
        # Rate here
        write_url(req['data']['URL'])
        run_scoring()
        with open("dict.txt") as fptr:
            dict_resp = json.loads(fptr.read())
        isIngest = ingestibilty(dict_resp)
        if (isIngest) is not True:
            cursor.close()
            return "Ingestibility failed. Package was not uploaded to database.", 403

        query = "UPDATE package SET ramp_up = %s, correctness = %s, bus_factor = %s, responsiveness = %s, license = %s, dependancy = %s, overall = %s  WHERE package_id = %s;"
        cursor.execute(query,(dict_resp['ramp_up'],dict_resp['correctness'],dict_resp['bus_factor'],dict_resp['responsiveness'],dict_resp['license'],dict_resp['dependency'],dict_resp['score'], req['metadata']['ID']))#dict_resp['correctness'],dict_resp['bus_factor'],dict_resp['responsiveness'],dict_resp['license'],dict_resp['dependency'],dict_resp['score'],id))
        
        cnx.commit()
        cursor.execute("SELECT * FROM package WHERE package_id = %s",(req['metadata']['ID'],))
        resp = pd.DataFrame(cursor.fetchall())
        resp.columns = cursor.column_names
        resp = resp.to_json(orient='records')

        
        uploadFiles(req['metadata']['ID'],req['data']['Content'])
        return resp[1:-1], 201
    else:
        cursor.close()
        return "Package ID already exists. Choose a different ID.", 403
    #return 'Creating package'


@app.route('/package/byName/<name>', methods = ['GET'])
@token_required
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
@token_required
def deletePackageByName(name): #essential
    cursor = cnx.cursor(buffered = True)
    cursor.execute("DELETE FROM package WHERE package_name = %s",(name,))
    cursor.execute("SELECT ROW_COUNT()")
    cnx.commit()
    if cursor.fetchone()[0] == 0:
        return 'Package not found', 400
    return 'Package Deleted',200

@app.route('/package/<id>/rate', methods = ['GET']) #essential
@token_required
def rate(id):
    
    cursor = cnx.cursor(buffered = True)
    cursor.execute(("SELECT * FROM package WHERE package_id = %s"),(id,))
    
    frame = pd.DataFrame(cursor.fetchall())
    if frame.empty:
        return 'No such package', 400
    frame.columns = cursor.column_names
    resp = frame.to_json(orient='records')
    req = json.loads(resp)
    a = req[0]['ramp_up']
    dict_ratings = {'RampUp' : req[0]['ramp_up'],
                    'Correctness' : req[0]['correctness'], 
                    'BusFactor' : req[0]['bus_factor'], 
                    'ResponsiveMaintainer' : req[0]['responsiveness'], 
                    'LicenseScore' : req[0]['license'],
                    'GoodPinningPractice' : req[0]['dependancy']}
    isIngestible = ingestibilty(dict_ratings)

    if isIngestible is not True:
        return 'The package rating system failed. Package not ingestible or rating failed.', 500

    return dict_ratings,200
    

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
