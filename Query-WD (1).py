import json
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Replace with your IBM Cloud API key and endpoint
api_key = '0IipvUSqpZb-IiZS13\6gfC'
service_url = 'https://api.us-south.discovery.watson.cloud.ibm.com/instances/04a74a82-53cb-\d195459'

# Specify your project ID
project_id = 'b499c3a3-53e9-43e0'

# Initialize the Watson Discovery service
authenticator = IAMAuthenticator(api_key)
discovery = DiscoveryV2(
    version='2021-04-30',
    authenticator=authenticator
)
discovery.set_service_url(service_url)



#Function to retrieve the collection ID within a project
def get_collection_id(project_id):
    try:
        response = discovery.list_collections(
            project_id=project_id
        ).get_result()

        # Assuming you have only one collection in the project, you can get the ID like this
        collection_id = response['collections'][0]['collection_id']
        print(collection_id)
        return collection_id

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Function to retrieve a list of document IDs in a collection
def list_documents_in_collection(collection_id):
    document_ids = []

    try:
        response = discovery.list_documents(
            project_id=project_id,
            collection_id=collection_id
        ).get_result()
        print(response)
        documents = response.get('documents', [])
        print(documents)
        for document in documents:
            print(document['document_id'])
            document_ids.append(document['document_id'])

        return document_ids

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

# Function to check document content by ID
def check_document_content(project_id, collection_id,document_id):
    try:
        response = discovery.get_document(
            project_id=project_id,
            collection_id=collection_id,
            document_id=document_id
        ).get_result()

        if response.get('status') == 'available':
            document = discovery.get_document(
                project_id=project_id,
                collection_id=collection_id,
                document_id=document_id
            ).get_result()
            # Print the document content
            print(json.dumps(document, indent=2))
        else:
            print(f"Document status: {response.get('status')}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def retrieve_document_by_id(project_id, document_id):
    try:
        # Construct a query that filters by document ID
        query = f'document_id:{document_id}'
        
        response = discovery.query(
            project_id=project_id,
            query=query
        ).get_result()

        # Check if any documents were found
        if response.get('matching_results', 0) > 0:
            # The document content can be found in the 'text' field of the first result
            document_content = response['results'][0]['text']
            return document_content
        else:
            print(f"No document found with ID: {document_id}")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None



## Get the collection ID within the project
collection_id = get_collection_id(project_id)

if collection_id:
    # Get a list of document IDs in the collection
    document_ids = list_documents_in_collection(collection_id)

    # Check content for each document
    for doc_id in document_ids:
        print(f"Checking document with ID: {doc_id}")
        print(collection_id)
        check_document_content(project_id,collection_id, doc_id)

        # Get the content of a document by its ID
        document_content = retrieve_document_by_id(project_id,doc_id)

        if document_content:
            # Print or use the document content as needed
            print(document_content)