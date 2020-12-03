import requests

with open('users.txt','r') as f:
    content = f.read().splitlines()

    for wms_id in content:
        url = "http://127.0.0.1:8000/auth/users/"

        payload={'wms_id': wms_id,
        'email': f'{wms_id}@ya.ru',
        'password': 'DNHnxvxF'}
        files=[

        ]
        headers = {
          'Authorization': 'Token bbf827f13006efde2a56d12239b39bffdc56fd9f'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)