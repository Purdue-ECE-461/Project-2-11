import requests
import json
import sys

def testAuth():
    url = "https://ece461proj2trustmoduleregistry.ue.r.appspot.com/authenticate"

    payload = json.dumps({
    "User": {
        "name": "Alfalfa",
        "isAdmin": True
    },
    "Secret": {
        "password": "sunt minim tempor"
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)

def testReset():

    url = "https://ece461proj2trustmoduleregistry.ue.r.appspot.com/reset"

    payload={}
    headers = {
    'X-Authorization': 'Lo'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response.text)

def testGetPackages():

    url = "http://127.0.0.1:8080/packages?offset=1"

    payload={}
    headers = {
    'X-Authorization': 'Lo',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

def testCreate():

    url = "https://ece461proj2trustmoduleregistry.ue.r.appspot.com/package"

    payload = json.dumps({
    "metadata": {
        "Name": "test_package2",
        "Version": "1.2.3",
        "ID": "deploy"
    },
    "data": {
        "Content": "ZGVjb2Rl",
        "URL": "ut esse Ut",
        "JSProgram": "fugiat eiusmod ut nulla proident"
    }
    })
    headers = {
    'X-Authorization': 'Lo',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def TestRate():

    url = "https://ece461proj2trustmoduleregistry.ue.r.appspot.com/package/deploy/rate"

    payload={}
    headers = {
    'X-Authorization': 'Lo'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

def testDelete():
    url = "https://ece461proj2trustmoduleregistry.ue.r.appspot.com/package/deploy"

    payload={}
    headers = {
    'X-Authorization': 'Lo'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response.text)

def testUpdate():

    url = "https://ece461proj2trustmoduleregistry.ue.r.appspot.com/package/deploy"

    payload = json.dumps({
    "metadata": {
        "Name": "dolore et culpa ullamco",
        "Version": "1.2.3",
        "ID": "23"
    },
    "data": {
        "Content": "nulla",
        "URL": "ut esse Ut",
        "JSProgram": "fugiat eiusmod ut nulla proident"
    }
    })
    headers = {
    'X-Authorization': 'Lo',
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)

def testRetrieve():
    url = "https://ece461proj2trustmoduleregistry.ue.r.appspot.com/package/deploy"

    payload={}
    headers = {
    'X-Authorization': 'Lo'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

if __name__ == "__main__":
    if (sys.argv[1] == "auth"):
        testAuth()
    elif (sys.argv[1] == "reset"):
        testReset()
    elif (sys.argv[1] == "get"):
        testGetPackages()
    elif (sys.argv[1] == "create"):
        testCreate()
    elif (sys.argv[1] == "rate"):
        TestRate()
    elif (sys.argv[1] == "delete"):
        testDelete()
    elif (sys.argv[1] == "update"):
        testUpdate()
    elif (sys.argv[1] == "retrieve"):
        testRetrieve()
    else:
        # run all functions
        testAuth()
        testReset()
        testGetPackages()
        testCreate()
        TestRate()
        testDelete()
        testUpdate()
        testRetrieve()
