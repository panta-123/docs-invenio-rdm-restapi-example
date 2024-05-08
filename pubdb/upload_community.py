import requests
import json

# Create via https://127.0.0.1:5000/account/settings/applications/tokens/new/
api = "https://inveniordm.jlab.org"
token = "Ick25gG6cagcmxaZNNRtt6KaLLpfV7qYIeHM67Ni7sIlsJSJmb1RKK5j1Pku"

# Define a list of records you want to upload:
# ('<record metadata json>.json', ['<datafile1>', '<datafile2>'])
records = [
    ('invenio_pub_all.json', ['1911.00295.pdf',])
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
datafile = "invenio_pub_all.json"
with open(datafile, 'r') as file:
    data = json.load(file)

failed_create_review = []
failed_submit_review = []
failed_accept = []
failed_publish = []
duplicate_record = []
data = data
for record in data:
    #proposal_number = record["custom_fields"]["pac:proposal_number"]
    #req = f'https://inveniordm.jlab.org/api/records?q=custom_fields.pac\\:proposal_number:"{proposal_number}"&l=list&p=1&s=10&sort=bestmatch'
    #res = requests.get(req)
    #if res.json()['hits']['total'] == 0:
    r = requests.post(f"{api}/api/records", data=json.dumps(record), headers=h,verify=True)
    if r.status_code == 201:
        print("success create draft")
        record_id = r.json()['id']
        review_request = f'{api}/api/records/{record_id}/draft/review'
        data = {"receiver": { "community": "b03bbb6c-8acd-400b-a239-d6a10558d482"},"type": "community-submission"}
        r = requests.put(review_request, data=json.dumps(data), headers=h,verify=True)
        if r.status_code == 200:
            print("success created review request")
            data = {"payload": {"content": "Thank you in advance for the review.","format": "html"}}
            submit_review = r.json()['links']['actions']['submit']
            r = requests.post(submit_review, data=json.dumps(data), headers=h,verify=True)
            if r.status_code in [202, 200]:
                print("success submit for review")
                accept_request = r.json()['links']['actions']['accept']
                data = {"payload": {"content": "You are in!", "format": "html"}}
                r = requests.post(accept_request, data=json.dumps(data), headers=h,verify=True)
                if r.status_code in [202, 200]:
                    print("success accepted")
                else:
                    print(r.status_code)
                    print("error accepting")
                    failed_accept.append(record)
            else:
                print(r.status_code)
                print(r.json())
                print("error submitting for review")
                failed_submit_review.append(record)
        else:
            print(r.json())
            print("error creating review request")
            failed_create_review.append(record)
    else:
        print("error creating draft")
        duplicate_record.append(record)
print(duplicate_record)
print(failed_create_review)
print(failed_submit_review)
print(failed_accept)
