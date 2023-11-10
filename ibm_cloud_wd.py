import json,os,jsonify
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Replace with your IBM Cloud API key and endpoint
wd_api_key = os.getenv("WD_API_KEY", None)
wd_service_url = os.getenv("WD_SERVICE_URL", None)
wd_project_id =os.getenv("WD_PROJECT_ID", None)
wd_version=os.getenv("WD_VERSION", None)         

def initialize_discovery(wd_api_key, wd_service_url):
    authenticator = IAMAuthenticator(wd_api_key)
    discovery = DiscoveryV2(
        version=wd_version,  # Use the latest version available at the time
        authenticator=authenticator
    )
    discovery.set_service_url(wd_service_url)
    return discovery

discovery=initialize_discovery(wd_api_key, wd_service_url)
#Function to retrieve the collection ID within a project
def get_collection_id(project_id):
    try:
        response = discovery.list_collections(
            project_id=project_id
        ).get_result()

        # Assuming you have only one collection in the project, you can get the ID like this
        collection_id = response['collections']
        # collection_id = response['collections'][0]['collection_id']
        print(collection_id)
        return collection_id

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def query_discovery_collection( project_id,collection_id, query):
    response = discovery.query(
    project_id=project_id,
        collection_ids=[collection_id],
        # collection_ids=['41fc4d63-e8f8-3456-0000-018bb774d6c5'],
        natural_language_query=query,
        count=2
    ).get_result()
    with open('discovery_response.json', 'w') as json_file:
        json.dump(response, json_file, indent=2)
    result=response
    passage_text_list = [passage["passage_text"] for result in result["results"] for passage in result["document_passages"]]
    # Print the list of passage_text values
    for passage_text in passage_text_list:
        print(passage_text)
    return response

def query_discovery( query):

    # discovery=initialize_discovery(wd_api_key, wd_service_url)
    response = discovery.query(
    project_id=wd_project_id,
        # collection_ids=['41fc4d63-e8f8-3456-0000-018bb774d6c5'],
        natural_language_query=query,
        count=3
    ).get_result()
    with open('discovery_response.json', 'w') as json_file:
        json.dump(response, json_file, indent=2)
    result=response
    passage_text_list = [passage["passage_text"] for result in result["results"] for passage in result["document_passages"]]
    print(passage_text_list)
    return passage_text_list


if __name__ == '__main__':

    # discovery = initialize_discovery(wd_api_key, wd_service_url)

    query ='product usp'
    # passages = query_discovery(discovery, wd_project_id, query, count=3)
    passages = query_discovery(query)
    collection_id='41fc4d63-e8f8-3456-0000-018bb774d6c5'
