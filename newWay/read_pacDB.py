import requests

pac_community_id = "e7d9d467-f3a2-4ef9-8bbf-200d51642df6"

url = 'https://misportal.jlab.org/pacProposals/proposals/download.json'

params = {
    'pac_number': '',
    'type_id': '',
    'submit_date_after': '03/05/2024',
    'submit_date_before': '',
    'modification_date': '08/05/2024'
}

def cleanedName(name):
    names = name.split()
    # The first name includes the middle name if present
    first_name = ' '.join(names[:-1])
    # Last name is the last element in the names list
    last_name = names[-1]
    return {"type": "personal", "given_name":first_name, "family_name":last_name}

meta = []
response = requests.get(url, params=params)

print(response.url)
if response.status_code == 200:
    data_dict = response.json()
    data = data_dict["data"]
    for entry in data:
        inveniodict = {"metadata": {"creators": [],"contributors":[]}}
        inveniodict["metadata"]["title"] = entry.get("title")
        inveniodict["metadata"]["resource_type"]= {"id": "publication-proposal"}
        inveniodict["metadata"]["publication_date"]= entry.get("submitted_date")
        if entry['contact_person']:
            contactNameDict = cleanedName(entry['contact_person'])
            contactdict = {"person_or_org":contactNameDict, 
                            "affiliations":[{"name":entry['contact_person']["institution"]}],
                            "role": {"id": "contactperson", "title": {"en": "Contact person"}}
                            }
            inveniodict["metadata"]["contributors"].append(contactdict)
        
        spokespersons = entry["spokespersons"]
        spokesList = []
        if spokespersons:
            for spokes in spokespersons:
                spokesNameDict = {"type": "personal", "given_name":spokes["first_name"], "family_name":spokes["last_name"]}
                spokesDict = {"person_or_org":spokesNameDict, 
                            "affiliations":[],
                            "role": {"id": "projectleader", "title": {"en": "Project leader"}}
                            }
                spokesList.append(spokesDict)
        inveniodict["metadata"]["contributors"] += spokesList

        if entry['authors']:
            author_list = []
            for author in entry['authors']:
                authorNameDict = {"type": "personal", "given_name":author["first_name"], "family_name":author["last_name"]}
                institution = author['institution']
                if not institution:
                    institution = "UNKNOWN"
                authdict = {"person_or_org":authorNameDict,
                            "affiliations":[{"name":institution}],
                            "role": {"id": "researcher", 
                                    "title": 
                                    {"en": "Researcher"}},}
                author_list.append(authdict)
            inveniodict["metadata"]["creators"] += author_list

        custom_fields = {
            "pac:pac_number": entry.get('pac_number', ""),
            "pac:beam_days": entry.get('beam_days', ""),
            "pac:proposal_number": entry.get("proposal_number",""),
            "pac:pac_status": entry.get("pac_status",""),
            "pac:pac_rating": entry.get("pac_rating",""),
            "pac:pacId": entry.get("id","")
            }
        if entry['experiment']:
            custom_fields["rdm:experiment_number"] = entry['experiment']["experiment_number"]
        if entry["links"]:
            html_record_url = entry["links"]["proposal_html_url"]
            json_record_url = entry["links"]["proposal_pdf_url"]
            isderivedfromdict =  { "identifier": html_record_url,
                                    "scheme": "url",
                                    "relation_type": {
                                        "id": "isderivedfrom",
                                        "title": {
                                            "de": "Wird abgeleitet von",
                                            "en": "Is derived from"
                                            }
                                    }
                                }
            inveniodict["metadata"]["related_identifiers"] = [isderivedfromdict]

        attachment_list = []
        if entry["attachments"]:
            for attachment in entry["attachments"]:
                attachment_url = attachment["links"]["document_url"]
                isdocumentedbydict = { "identifier": attachment_url,
                                    "scheme": "url",
                                    "relation_type": {
                                        "id": "isdocumentedby",
                                        "title": {
                                            "de": "Wird dokumentiert von",
                                            "en": "Is documented by"
                                        }
                                    }
                                }
                inveniodict["metadata"]["related_identifiers"] += [isdocumentedbydict]

        inveniodict["access"] =  {"files": "public", "record": "public", "embargo": {"active": False}}
        inveniodict["files"] = {"enabled": False}
        inveniodict["custom_fields"]= custom_fields
        inveniodict["parent"] =  {"communities": {
                                "default": pac_community_id,
                                "ids": [
                                    pac_community_id
                                    ]
                                }
                                },
        inveniodict["metadata"]["rights"]= [
            {
            "icon": "cc-by-icon","id": "cc-by-4.0",
                "props": {
                "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
                "scheme": "spdx"
                },
                "title": {
                "en": "Creative Commons Attribution 4.0 International"
                },
                "description": {
                "en": "The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the condition that the creator is appropriately credited."
                }
            }
            ]
        meta.append(inveniodict)

else:
    print('Error:', response.status_code)
