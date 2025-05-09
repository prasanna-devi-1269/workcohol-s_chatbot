# import json
# import PyPDF2
# import pandas as pd

# def read_file(file):
#     ext = file.name.split('.')[-1].lower()
#     if ext == "txt":
#         return file.read().decode("utf-8")
#     elif ext == "pdf":
#         reader = PyPDF2.PdfReader(file)
#         return "\n".join([page.extract_text() for page in reader.pages])
#     elif ext == "json":
#         data = json.load(file)
#         return json.dumps(data, indent=2)
#     elif ext == "csv":
#         df = pd.read_csv(file)
#         return df.to_string()
#     else:
#         return "Unsupported file type."

# def json_to_text(data):
#     """Flatten JSON to a readable text for embedding."""
#     return json.dumps(data, indent=2)

# def search_json_data(query, data):
#     """
#     Search through JSON data recursively to find relevant information.
#     """
#     def search_recursive(obj, query, path=""):
#         results = []
#         query = query.lower()
        
#         if isinstance(obj, dict):
#             for key, value in obj.items():
#                 current_path = f"{path}.{key}" if path else key
#                 # Check if query matches key
#                 if query in key.lower():
#                     results.append(f"{key}: {value}")
#                 # Recursively search values
#                 results.extend(search_recursive(value, query, current_path))
                
#         elif isinstance(obj, list):
#             for i, item in enumerate(obj):
#                 current_path = f"{path}[{i}]"
#                 if isinstance(item, (dict, list)):
#                     results.extend(search_recursive(item, query, current_path))
#                 elif isinstance(item, str) and query in item.lower():
#                     results.append(str(item))
                    
#         elif isinstance(obj, str) and query in obj.lower():
#             results.append(f"{path}: {obj}")
            
#         return results

#     # Convert query to lowercase for case-insensitive search
#     results = search_recursive(data, query)
    
#     if results:
#         return "\n".join(results)
#     return "No relevant information found in the dataset."
import json
import PyPDF2
import pandas as pd

def read_file(file):
    ext = file.name.split('.')[-1].lower()
    if ext == "txt":
        return file.read().decode("utf-8")
    elif ext == "pdf":
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])
    elif ext == "json":
        data = json.load(file)
        return json.dumps(data, indent=2)
    elif ext == "csv":
        df = pd.read_csv(file)
        return df.to_string()
    else:
        return "Unsupported file type."

def search_json_data(query, data):
    context = ""
    for item in data:
        if query.lower() in json.dumps(item).lower():
            context += json.dumps(item, indent=2) + "\n"
    return context or "No relevant info found in the dataset."

