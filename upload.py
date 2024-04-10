import requests
import json

# Create via https://127.0.0.1:5000/account/settings/applications/tokens/new/
api = "https://inveniordm.jlab.org"
token = "L12EgU9Zus1iVHOSeF6iPddGA4t4mgfHGenDKQujWsZvBq6MvaYMb3ZlkD5c"

# Define a list of records you want to upload:
# ('<record metadata json>.json', ['<datafile1>', '<datafile2>'])
records = [
    ('1.json', ['1911.00295.pdf',])
]
# 1911.00295.pdf -> http://www.jlab.org/exp_prog/proposals/06/PR12-06-101.pdf

#
# HTTP Headers used during requests
#
h = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
fh = {
    "Accept": "application/json",
    "Content-Type": "application/octet-stream",
    "Authorization": f"Bearer {token}"
}

"""
# Upload and publish all records.
#
for datafile, files in records:
    # Load the record metadata JSON file.
    with open(datafile) as fp:
        data = json.load(fp)
    print(json.dumps(data))
    # Create the record
    # note: "verify=False" is so that we can connect to 127.0.0.1 with a
    # self-signed certificate. You should not do this in production.
    r = requests.post(
        f"{api}/api/records", data=json.dumps(data), headers=h)
    print(r.reason )
    assert r.status_code == 201, \
        f"Failed to create record (code: {r.status_code})"
    links = r.json()['links']
    r = requests.post(links["publish"], headers=h, verify=True)
    print(r.json())
    assert r.status_code == 202, f"Failed to publish record (code: {r.status_code})"
    print(links)
"""
datafile = "1.json"
with open(datafile, 'r') as file:
    data = json.load(file)

failed_create = []
failed_publish = []
duplicate_record = []
for record in data:
    proposal_number = record["custom_fields"]["pac:proposal_number"]
    req = f'https://inveniordm.jlab.org/api/records?q=custom_fields.pac\\:proposal_number:"{proposal_number}"&l=list&p=1&s=10&sort=bestmatch'
    res = requests.get(req)
    if res.json()['hits']['total'] == 0:
        r = requests.post(f"{api}/api/records", data=json.dumps(record), headers=h,verify=True)
        if r.status_code == 201:
            print("success create ")
            links = r.json()['links']
            r = requests.post(links["publish"], headers=h, verify=True)
            if r.status_code == 202:
                print("success publish ")
            else:
                print("error publishing")
                failed_publish.append(record)
        else:
            failed_create.append(record)
    else:
        print("duplicate record skipped")
        duplicate_record.append(record)
print(failed_create)
print(failed_publish)
print(len(duplicate_record))
    #assert r.status_code == 201, \
    #    f"Failed to create record (code: {r.status_code})"
    
    
    #assert r.status_code == 202, f"Failed to publish record (code: {r.status_code})"

"""
    # Upload files
    for f in files:
        # Initiate the file
        data = json.dumps([{"key": f}])
        r = requests.post(links["files"], data=data, headers=h, verify=False)
        assert r.status_code == 201, \
            f"Failed to create file {f} (code: {r.status_code})"
        file_links = r.json()["entries"][0]["links"]

        # Upload file content by streaming the data
        with open(f, 'rb') as fp:
            r = requests.put(
                file_links["content"], data=fp, headers=fh, verify=False)
        assert r.status_code == 200, \
            f"Failed to upload file contet {f} (code: {r.status_code})"

        # Commit the file.
        r = requests.post(file_links["commit"], headers=h, verify=False)
        assert r.status_code == 200, \
            f"Failed to commit file {f} (code: {r.status_code})"

    # Publish the record
    r = requests.post( links["publish"], headers=h, verify=False)
    assert r.status_code == 202, \
            f"Failed to publish record (code: {r.status_code})"
"""
   

