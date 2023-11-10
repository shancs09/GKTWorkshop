import requests
import json,os,jsonify
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Replace with your IBM Watson Assistant credentials and Assistant ID
wa_api_key =  os.getenv("WA_API_KEY", None)
wa_assistant_id =  os.getenv("WA_ASSISTANT_ID", None)
wa_url =  os.getenv("WA_URL", None)
wa_version =  os.getenv("WA_VERSION", None)
wa_env_id=os.getenv("WA_ENVIRONEMNT_ID", None)

authenticator = IAMAuthenticator(wa_api_key)
assistant = AssistantV2(
    version=wa_version,
    authenticator=authenticator
)

assistant.set_service_url(wa_url)

def list_assistant():
    response=assistant.list_assistants().get_result()
    print(response)
def list_environment():
    response=assistant.list_environments(
        assistant_id=wa_assistant_id
        ).get_result()
    print(response)


def chat_with_assistant(query):
    response = assistant.message_stateless(
        assistant_id=wa_env_id,
        input={
            'message_type': 'text',
            'text': query
                }
    ).get_result()
    result=json.dumps(response, indent=2)
    print(json.dumps(response, indent=2))

    generic = response["output"]["generic"][0]
    print(generic)
    response_type = generic["response_type"]
    text = generic["text"]
    response_data = {
        "Response Type": response_type,
        "Text": text
    }
    return response_data

if __name__ == '__main__':

    query ='tell me about borrower detail'
    passages = chat_with_assistant(query)
