import requests
import json
import sys

def postMessage(midi_file):
    authkey = "Bearer xoxp-672670374340-709681237543-701524491505-cd8aae979ae71c4809b442a821d59ccc"
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Content-Type":"application/json", "Authorization":authkey}

    body = {'text':'sing {}'.format(midi_file), 'channel':"#m5stackxcozmo"}

    response = requests.post(url, data=json.dumps(body), headers=headers)
    return json.dumps(response)