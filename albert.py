# import requests

# # Define the API endpoint and subscription key
# url = "https://translation-api.ghananlp.org/tts/v1/tts"
# subscription_key = "ac22989547f04e979df0b7e89beed41b"

# # Define the headers
# headers = {
#     "Content-Type": "application/json",
#     "Cache-Control": "no-cache",
#     "Ocp-Apim-Subscription-Key": subscription_key
# }

# # Define the payload
# payload = {
#     "text": "Ɛte sɛn?",
#     "language": "tw"

import requests
import urllib
import json
import logging


# Configure logging
logger = logging.getLogger(__name__)

def translate_to_twi(message):
    url = "https://translation-api.ghananlp.org/v1/translate"
    hdr = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': '8cf25ed739154351906128c0cb623a71',
    }
    data = {
        "in": message,
        "lang": "tw-en"
    }
    data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, headers=hdr, data=data)

    try:
        response = urllib.request.urlopen(req)
        # response_data = json.loads(response.read())
        translated_text = response.read().decode('utf-8')
        return translated_text
    except urllib.error.HTTPError as e:
        logger.error(f'HTTP error: {e.code} - {e.reason}')
        return "Error HTTP translating the message"
    except urllib.error.URLError as e:
        logger.error(f'URL error: {e.reason}')
        return "Error URL translating the message"
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        return "Error UNEX translating the message"
    
    
    
ken =translate_to_twi("wo ho te sɛn")

print(ken)
