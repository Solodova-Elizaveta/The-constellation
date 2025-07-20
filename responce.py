import requests
import os
# API Configuration
def api_response(user_promt = '', api_key='',url=''):

    # Request payload configuration
    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": user_promt
    }

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key  # Authentication key from environment variable
    }

    
        # Send API request
    response = requests.request("POST", url, json=payload, headers=headers)
    response.raise_for_status()  # Raise exception for bad status codes
    answ = response.json()['outputs'][0]['outputs']
    ai_message = tuple(answ[0]['results']['message']['data']['text'])
    questions = tuple(answ[1]['results']['message']['data']['text'].split(';'))
    return answ+questions
    # Print response



