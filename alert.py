import requests

def sendAlert(message):
  url = "https://discord.com/api/webhooks/983167171398074368/OuLxr0yzdrf_JwsvXxi7qieGb40FySRQYePkI49flMhsTID9RuknYemPbwpDQwHCq2Fl"
  json_request = {
    "name": "Resuolve Alert",
    "type": 1,
    "channel_id": "199737254929760256",
    "token": "3d89bb7572e0fb30d8128367b3b1b44fecd1726de135cbe28a41f8b2f777c372ba2939e72279b94526ff5d1bd4358d65cf11",
    "avatar": '',
    "guild_id": "199737254929760256",
    "id": "223704706495545344",
    "content": f"{message}",
    "application_id": ''
  }

  requests.post(url, json=json_request)
