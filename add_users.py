import requests

with open('users.txt', 'r') as f:
    content = f.read().splitlines()

    for wms_id in content:
        url = "http://127.0.0.1:8000/auth/users/"

        payload={'wms_id': wms_id,
        'email': f'test-{wms_id}@yandex.ru',
        'password': 'DNHnxvxF'}
        files=[

        ]
        headers = {

        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)