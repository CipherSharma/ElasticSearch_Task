from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
from pymongo.errors import OperationFailure

client = MongoClient("mongodb+srv://Cipher:Tushar@0380@cluster0.qabsj.mongodb.net/?retryWrites=true&w=majority")
db_handle=client["Test"]
MetaData_handle = db_handle['MetaData']

def search(query):
    try:
        # Define the search pipeline
        results = MetaData_handle.aggregate([
            {
                "$search": {
                    "index":"matching_search",
                    "compound":{
                        "must":[
                            {    
                                "text": {
                                    "query": query,
                                    "path": ["Title", "Category", "SubCategory"],
                                }
                            },
                        ],
    
                        "should":[
                            {
                                "text":{
                                    "query": "N",
                                    "path": "ParentExists",
                                    "score":{"boost":{"value":5}}
                                }
                            },
                            {
                                "text":{
                                    "query": "Y",
                                    "path": ["ParentExists","Child"],
                                    "score":{"boost":{"value":4}}
                                }
                            },
                            
                        ],
    
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "Title": 1,
                    "Category": 1,
                    "SubCategory": 1,
                    "ParentExists": 1,
                    "Child": 1,
                    "score":{"$meta":"searchScore"},
                }
            },
        ])

        # Execute the search query
       

        # Extract relevant fields
        relevant_results = []
        for result in results:
            relevant_results.append({
                "Title": result["Title"],
                "Category": result["Category"],
                "SubCategory": result["SubCategory"],
                "ParentExists":result["ParentExists"],
                "Child":result["Child"],
                "score": result["score"],
            })

        return relevant_results
    except OperationFailure as e:
        print(f"Error executing search: {e}")
 

@api_view(["POST"])
def search_data(request):
    try:
        data=request.data
        query=data["query"]
        result=search(query)
        return Response({"Search Results":result}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Response":"error is "+str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)


