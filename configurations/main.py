import requests
import json

request = requests.Session()
request.headers.update({'X-API-KEY': 'edd1c9f034335f136f87ad84b625c8f1'})

data = json.dumps({
    "username": "jackd",
    "plugins": {
        "jwt-auth": {
            "key": "user-key",
            "secret": "my-secret-key"
        }
    }
})

# response = request.put('http://apisix:9180/apisix/admin/consumers',data=data)
response = request.get('https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com')
print(response.headers)

