import requests
import json

# Create via https://127.0.0.1:5000/account/settings/applications/tokens/new/
api = "https://inveniordm.jlab.org"
token = "xQkHtzcEUfSLiTCjGDOFtL1fI9Z3R6niOaAEYzG3XHxJ0csDw2Zj7fOYqBqJ"
pub_community_id = "03cfbd45-6332-4680-9960-939ed7a2c3b9"


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


failed_create_review = []
failed_submit_review = []
failed_accept = []
failed_publish = []
duplicate_record = []

def upload(data):
    for record in data:
        pubID = record["custom_fields"]["pac:pacID"]
        req = f'https://inveniordm.jlab.org/api/records?q=custom_fields.pac\\:pacID:"{pubID}"&l=list&p=1&s=10&sort=bestmatch'
        res = requests.get(req)
        if res.json()['hits']['total'] == 0:
            r = requests.post(f"{api}/api/records", data=json.dumps(record), headers=h,verify=True)
            if r.status_code == 201:
                print("success create draft")
                record_id = r.json()['id']
                review_request = f'{api}/api/records/{record_id}/draft/review'
                data = {"receiver": { "community": pub_community_id},"type": "community-submission"}
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