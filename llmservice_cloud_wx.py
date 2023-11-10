import requests,os
from flask import Flask, request, jsonify,Response
from ibm_cloud_sdk_core import IAMTokenManager
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator, BearerTokenAuthenticator

# IBM CLOUD - IAM API Credentials
cloud_api_key = os.getenv("IAM_API_KEY", None)
# EndPoints
wx_ga_host=os.getenv("WX_GA_HOST", None)
auth_url=os.getenv("IAM_AUTH_URL", None)
# WatsonStudio/ CloudPak Saas
project_id= os.getenv("WX_PROJECT_ID", None)


# Endpoint Url
wx_endpoint_url= wx_ga_host + "/ml/v1-beta/generation/text?version=2023-05-29"
wx_access_token = IAMTokenManager(
                            apikey = cloud_api_key,
                            url = auth_url
                            ).get_token()

# Authentication header
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+wx_access_token
}

def generate_campaign(input_text,temp):
    #Set input text
    llmInput=input_text
    # Instruction
    instruction="Generate a 5 sentence marketing message for a company with the given characteristics."
    
    if temp==0:
        decoding_method="greedy"
    else:
        decoding_method="sample"

    #Parameters
    parameters = { "decoding_method": decoding_method, 
                   "max_new_tokens": 200,  
                   "min_new_tokens": 1,  
                   "random_seed": 111, 
                     "stop_sequences": [],  
                     "temperature": temp,
                    #  "temperature": 0.8,  "top_k": 50,  "top_p": 1,  
                     "repetition_penalty": 2 }

    #Payload
    # inputs=instruction+' '+llmInput
    # print(inputs)
    llmPayload = {
                "model_id": "google/flan-ul2", 
                "input":instruction+' '+llmInput, 
                # "template":template,
                "parameters": parameters,
                "project_id": project_id
            }

    print(parameters)
    print("Calling Campaign Generation ...")
    response = requests.post(wx_endpoint_url, json=llmPayload, headers=headers)
    print(response.json())
    response=response.json()
    if "results" in response:
        generated_text=response['results'][0]['generated_text']
        print(generated_text)
        return generated_text
    else:
        erro_message=response['message']
        return erro_message

if __name__ == '__main__':
    input_doc="Company Information: Federal Bank Product/Service Description: Savings Account Key Benefits: 1. Quick and easy online account opening with just a few clicks. 2. High annual interest rate of 1.75%. 3. No monthly maintenance fees. 4. Access to online banking and mobile app for account management. 5. Minimum initial deposit of $1,000. 6. FDIC insured up to $250,000 per account. 7. Account available for individuals aged 18 and above."
    generate_campaign(input_doc,0.7)
