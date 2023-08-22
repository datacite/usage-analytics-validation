import requests
import base64
import gzip
import io

# Function to retrieve a report from the usage reports api based upon it's unique identifier
def get_report(report_id):
    # Define the usage reports API url
    url = 'https://api.datacite.org/reports/' + report_id

    # Make a request to the usage reports API
    response = requests.get(url)

    # Turn the response into a JSON object
    response_json = response.json()

    # Get the gzip data from first entry in report subsets
    gzip_data = response_json['report']['report-subsets'][0]['gzip']

    # Gzip data is base64 encoded
    # Decode the gzip data
    gzip_data = base64.b64decode(gzip_data)

    decompress_and_save(gzip_data, report_id)

def decompress_and_save(compressed_data, filename):
    filename = 'data/' + filename + '.json'

    with gzip.GzipFile(fileobj=io.BytesIO(compressed_data), mode='rb') as gzip_file:
        decompressed_json = gzip_file.read().decode('utf-8')
        with open(filename, 'w') as output_file:
            output_file.write(decompressed_json)

if __name__ == '__main__':
    get_report('7898f875-dabe-4ec8-a857-7f81fd30c242')