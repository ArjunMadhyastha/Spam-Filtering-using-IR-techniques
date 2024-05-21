import pandas as pd
import json

# Replace 'your_data.csv' with the actual path of your CSV file
csv_file_path = 'dataset.csv'
df = pd.read_csv(csv_file_path)

# Assuming your CSV file has columns 'URL' and 'Label', modify these column names if needed
url_col = 'URL'
label_col = 'Label'

# Create a dictionary to store document content
document_contents = {}

# Iterate through the rows of the DataFrame and populate the dictionary
for index, row in df.iterrows():
    url = row[url_col]
    label = row[label_col]
    # Modify the URL to use the "Document_" format
    document_id = f"Document_{index + 1}"
    document_contents[document_id] = label

# Save the dictionary to a JSON file
json_file_path = 'document_contents.json'
with open(json_file_path, 'w') as json_file:
    json.dump(document_contents, json_file, indent=2)

print(f"Document contents saved to {json_file_path}")
