import requests


def alert(x):
    url = "https://discord.com/api/webhooks/965389495476310069/oYm8pcDZ9g15kwEpRDUp_P6pZYChnClIUIqYHqEnC-jbVckAs8BBZxw5ELch6WyKswpZ"
    json_request = {
        "name": "Resuolve Alert",
        "type": 1,
        "channel_id": "199737254929760256",
        "token": "3d89bb7572e0fb30d8128367b3b1b44fecd1726de135cbe28a41f8b2f777c372ba2939e72279b94526ff5d1bd4358d65cf11",
        "avatar": '',
        "guild_id": "199737254929760256",
        "id": "223704706495545344",
        "content": f"Seu servidor {x}",
        "application_id": ''
    }

    return requests.post(url, json=json_request)
