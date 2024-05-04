import glob
import json
import re
from datetime import datetime

def cleanedName(name):
    names = name.split()
    # The first name includes the middle name if present
    first_name = ' '.join(names[:-1])
    # Last name is the last element in the names list
    last_name = names[-1]
    return {"type": "personal", "given_name":first_name, "family_name":last_name}

division_title_id = {
    "Exp Nuclear Physics / Technical Support Groups / Cryo/Polarized Targets": "ENPTSG-CP",
    "Exp Nuclear Physics / Technical Support Groups / Fast Electronics": "ENPTSG-FE",
    "Exp Nuclear Physics / Technical Support Groups / Detector": "ENPTSG-DET",
    "Exp Nuclear Physics / Technical Support Groups / Data Acquisition": "ENPTSG-DA",
    "Exp Nuclear Physics / Technical Support Groups / User Liaison": "ENPTSG-UL",
    "Exp Nuclear Physics / Technical Support Groups / Cryo/Polarized Targets": "ENPTSG-CT",
    "Exp Nuclear Physics / Physics Division Office / Administrative": "ENPH-PDO-ADMIN",
    "Exp Nuclear Physics / Physics Division Office / Phys Div Univ Relations": "ENPH-PDO-PDUR",
    "Exp Nuclear Physics / Experimental Halls / Physics Magnet": "ENPH-EH-PM",
    "Exp Nuclear Physics / Experimental Halls / Hall A": "ENPH-EH-HA",
    "Exp Nuclear Physics / Experimental Halls / Hall B": "ENPH-EH-HB",
    "Exp Nuclear Physics / Experimental Halls / Hall C": "ENPH-EH-HC",
    "Exp Nuclear Physics / Experimental Halls / Hall D": "ENPH-EH-HD",
    "Exp Nuclear Physics / Experimental Halls / Physics EIC": "ENPH-EHPH",
    "Accelerator Ops, R&D / Inst for SRF Sci & Tech / Operations Support": "AORD-ISST-OS",
    "Accelerator Ops, R&D / Inst for SRF Sci & Tech / SRF CM Production": "AORD-ISST-SRF-CMP",
    "Chief Scientist Office / Chief Scientist Office / Chief Scientist Office": "CSO-CSO-CSO",
    "ES&H Division / ES&H Division / ESH&Q Division": "ESHD-ESHQ",
    "Directorate / Directorate / Directorate": "DIR-DIR-DIR",
    "Comp Sci&Tech (CST) Div / Data Science / Data Science": "CSDS-DS",
    "ES&H Division / ES&H Division / Radiation Control": "ESHD-RAD-CTRL",
    "ES&H Division / ES&H Division / ESH Division Leadership": "ESHD-ESHQ-LEAD",
    "Accelerator Ops, R&D / Accelerator Operations / Operations": "AORD-OPS",
    "Accelerator Ops, R&D / Inst for SRF Sci & Tech / SRF Processes & Materials": "AORD-ISST-SRF-PM",
    "Accelerator Ops, R&D / Accelerator Operations / Ops Injector Group": "AORD-OPS-INJ-GP",
    "Accelerator Ops, R&D / Cntr-Adv Studies of Acce / Ctr for Adv Stud of Accel": "AORD-CASAC-CASAC",
    "Chief Operting Officr Off / Human Resources &Services / Science Education": "COO-HRS-SE",
    "Accelerator Ops, R&D / Inst for SRF Sci & Tech / SRF Research & Dev": "AORD-ISST-SRF-RD",
    "Engineering Division / Electrical Systems / EES Support Services": "ENG-EES-SSS",
    "Accelerator Ops, R&D / Inst for SRF Sci & Tech / SRF Test & Measurement": "AORD-ISST-SRF-TM",
    "Engineering Division / Mechanical Systems / Mechanical Engineering": "ENG-MS-ME",
    "Accelerator Ops, R&D / Accelerator Operations / Analysis & High-Level App": "AORD-OPS-AHAA",
    "Accelerator Ops, R&D / Inst for SRF Sci & Tech / SRF Engineering": "AORD-ISST-SRF-ENG",
    "Engineering Division / Electrical Systems / EES RF Systems": "ENG-EES-RFS",
    "Engineering Division / Electrical Systems / EES I&C Systems":"ENG-EES-ICS",
    "Accelerator Ops, R&D / Inst for SRF Sci & Tech / SRF Cavity Production": "AORD-ISST-SRF-CP",
    "Accelerator Ops, R&D / Inst for SRF Sci & Tech / SRF Special Projects": "AORD-ISST-SRF-SP",
    "Accelerator Ops, R&D / Inst for SRF Sci & Tech / SRF Science & Technology": "AORD-ISST-SRF-ST",
    "Engineering Division / Mechanical Systems / Cryogenics": "ENG-MS-CRY",
    "Accelerator Ops, R&D / Accelerator Operations / Accel Ops Dept Mgt": "AORD-OPS-AODM",
    "Accelerator Ops, R&D / Ctr For Injectors&Sources / Ctr for Injectors&Sources": "AORD-CIS-CIS",
    "Theory & Comp Physics / THEORY CENTER / THEORY CENTER": "TCP-TC-TC",
    "Accelerator Ops, R&D / Accelerator Operations / Accel Computing Group": "AORD-OPS-ACG",
    "Accelerator Ops, R&D / Accel Division Office / Accel Division Management": "AORD-ADO-ADM",
    "Accelerator Ops, R&D / Accelerator Operations / Ops Admin Group":"AORD-OPS-OA",
    "Comp Sci&Tech (CST) Div / Comp Sci&Tech Div Office / Comp Sci&Tech Div Office": "CSDS-CS-TD-O",
    "Comp Sci&Tech (CST) Div / Scientific Computing / Scientific Computing": "CSDS-CS-SC",
    "Accelerator Ops, R&D / Inst for SRF Sci & Tech / SRF Project Support":"AORD-ISST-SRF-PS"
}


# Get a list of JSON files matching the pattern "*.json"
json_files = glob.glob('/Users/panta/pubdb/*.json')
print(json_files)
meta = []

# Loop through each JSON file and load its contents
for file_name in json_files:
    with open(file_name, 'r') as f:
        record_dict = {}
        data = json.load(f)['data']
        for entry in data:
            inveniodict = {"metadata": {"creators": [],"contributors":[]}}
            submit_date = entry['submit_date']
            date_obj = datetime.strptime(submit_date, "%m/%d/%Y")
            submit_formatted_date = date_obj.strftime("%Y-%m-%d")
            inveniodict["metadata"]["publication_date"] = submit_formatted_date

            submitter_name = entry['submitter_name']
            if submitter_name:
                submitter_cleaned_name = re.sub(r'\([^)]*\)', '', submitter_name).strip()
                submitterNameDict = cleanedName(submitter_cleaned_name)
            #inveniodict["metadata"]["creators"]["person_or_org"] = submitterNameDict

            tile_name = entry['title']
            inveniodict["metadata"]["title"] = tile_name

            abstract = entry['abstract']
            inveniodict["metadata"]["description"] = abstract
            if 'document_type' in entry:
                document_type = entry['document_type']
                if document_type.lower() == "journal article":
                    inveniodict["metadata"]["resource_type"] = {"id": "publication-article",
                                                                "title": {
                                                                    "de": "Zeitschriftenartikel",
                                                                    "en": "Journal article"
                                                                    }
                                                                }
                elif document_type.lower() == "thesis":
                    inveniodict["metadata"]["resource_type"] = {"id": "publication-thesis",
                                                                "title": {
                                                                    "de": "Abschlussarbeit",
                                                                    "en": "Thesis"
                                                                    }
                                                                }
                    advisorList= entry["theses"]
                    if advisorList:
                        author_invenio_list = []
                        for advisor in advisorList:
                            advisor_name = advisor["advisor"]
                            advisor_affiliation = advisor['institution']
                            if advisor_name:
                                advisorNameDict = cleanedName(advisor_name)
                                advidict = {"person_or_org":submitterNameDict,
                                        "role": {"id": "supervisor",
                                                "title": {
                                                    "de": "SupervisorIn",
                                                    "en": "Supervisor"
                                                    }},}
                                author_invenio_list.append(advidict)
                        inveniodict["metadata"]["contributors"].append(advisorNameDict)

                elif document_type.lower() == "book":
                    inveniodict["metadata"]["resource_type"] = {"id": "publication-book",
                                                                "title": {
                                                                    "de": "Buch",
                                                                    "en": "Book"
                                                                    }
                                                                }
                elif document_type.lower() == "meeting":
                    inveniodict["metadata"]["resource_type"] = {"id": "other",
                                                                "title": {
                                                                    "de": "Sonstige",
                                                                    "en": "Other"
                                                                    }
                                                                }
                elif document_type.lower() == "other":
                    inveniodict["metadata"]["resource_type"] = {"id": "other",
                                                                "title": {
                                                                    "de": "Sonstige",
                                                                    "en": "Other"
                                                                    }
                                                                }

            #if 'document_subtype' in entry:
            #    inveniodict["metadata"]["resource_type"] = {"id": "document"

            publication_date = entry['publication_date']

            primary_institution = entry['primary_institution']
            division = entry['affiliation']
            try:
                divisonid = division_title_id[division]
                custom_fields = {
                "rdm:division": [
                    {
                        "id": divisonid,
                        "title": {
                            "en": division
                            }
                    }
                ],
                }
            except Exception as err:
                custom_fields = {}
                print(division)
            

            if entry['experiments']:
                custom_fields["rdm:experiment_number"] = ""
                for experiment in entry['experiments']:
                    expid = experiment['paperid']
                    custom_fields["rdm:experiment_number"] += expid + " "

            if entry['authors']:
                author_list = []
                for author in entry['authors']:
                    author_name = author['name']
                    if author_name:
                        authorNameDict = cleanedName(author_name)

                        institution = author['institution']
                        institution_fullname = author['institution_fullname'].split(",", 1)[0]
                        authdict = {"person_or_org":authorNameDict, 
                                    "affiliations":[{"name":institution_fullname}],
                                    "role": {"id": "researcher", 
                                            "title": 
                                            {"de": "WissenschaftlerIn",
                                            "en": "Researcher"}},}
                        author_list.append(authdict)
                inveniodict["metadata"]["creators"] += author_list

            if entry["links"]:
                html_record_url = entry["links"]["html_record_url"]
                json_record_url = entry["links"]["json_record_url"]
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

            jlab_number = entry["jlab_number"]
            if jlab_number:
                custom_fields["rdm:jlab_number"] = jlab_number
            osti_number = entry["osti_number"]
            if osti_number:
                custom_fields["rdm:osti_number"] = osti_number
            lanl_number = entry["lanl_number"]
            if lanl_number:
                custom_fields["rdm:lanl_number"] = lanl_number
             

            attachment_list = []
            if entry["attachments"]:
                for attachment in entry["attachments"]:
                    attachment_url = attachment["url"]
                    attachment_name = attachment["name"]
                    attachment_type = attachment["type"]
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
                    attachment_list.append({
                        "url": attachment_url,
                        "name": attachment_name,
                        "type": attachment_type
                    })

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
            inveniodict["access"] =  {"files": "public", "record": "public", "embargo": {"active": False}}
            inveniodict["files"] = {"enabled": False}
            inveniodict["custom_fields"]= custom_fields
            if "ldrd_funding" in entry:
                if entry["ldrd_funding"].lower() == "yes":
                    inveniodict["custom_fields"]["rdm:isldrd"] = True
                if entry["proposals"]:
                    for proposal in entry["proposals"]:
                        ldrd_num = proposal["proposal_num"]
                        inveniodict["custom_fields"]["rdm:ldrd_number"] = ldrd_num
            meta.append(inveniodict)


print(meta[2])
with open('invenio_pub_all.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=4)
