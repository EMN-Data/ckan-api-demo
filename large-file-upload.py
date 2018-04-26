import requests
import json
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from clint.textui.progress import Bar as ProgressBar

def update_progress(encoder):
    encoder_len = encoder.len
    bar = ProgressBar(expected_size=encoder_len, filled_char='=')

    def callback(monitor):
        bar.show(monitor.bytes_read)

    return callback

# Helper to build a URI for a given API action
action = lambda a: 'https://dev-datahub.h2awsm.org/api/3/action/{}'.format(a)

# Set your API token
api_token = '' #TODO

auth_header = {'authorization': api_token}

post_headers = {
    'authorization': api_token,
    'content-type': 'application/json;charset=utf-8'
}

def upload(filename, metadata):
    print('Uploading \n{}'.format(json.dumps(metadata, indent=2)))
    metadata['upload'] = (filename, open(filename, 'rb'))
    m = MultipartEncoder(fields=metadata)
    monitor = MultipartEncoderMonitor(m, update_progress(m))
    r = requests.post(action('resource_create'),
        data=monitor,
        headers={
            'Authorization': api_token,
            'Content-Type': m.content_type
        })
    print('Status: {}\n'.format(r.status_code))
    print r.reason
    return r

resource_metadata = {
    'package_id': '07a48d23-0025-4720-b2ca-841527fc3fd8',
    'name': '1GB-file'
}

if __name__ == "__main__":
    # upload('/Users/nwunder2/Projects/emn/ckan-api-demo/data/100MB.img', data=resource)
    upload('/Users/nwunder2/Projects/emn/ckan-api-demo/data/1GB.img', metadata=resource_metadata)
