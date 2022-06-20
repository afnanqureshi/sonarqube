'''
    This code generates a report of Last Analysis Date along with owners for
    projects in SonarQube.
    __author__ = "Mohd Afnan Qureshi"
    __maintainer__ = "Mohd Afnan Qureshi"
    __email__ = "md.afnan1995@gmail.com"
    __status__ = "Production"
'''

import requests
import json
import math
import re
from urllib3.exceptions import InsecureRequestWarning
import os

# Global variable declaration
SQ_env = "sonarqube.com"
SQ_token = os.getenv('token')
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + SQ_token
}


# Method to get name and key pattern details from Permission Template
def getptData():
    ptlist = {}
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.get("https://" + SQ_env + "/api/permissions/search_templates", headers=headers, verify=False)
    data = json.loads(response.text)
    for d in (data['permissionTemplates']):
        if d['name'] == 'Default template':
            print()
        else:
            name = d['name']
            name = name.split()
            name = name[0]
            name = name + "-admins"
            if 'projectKeyPattern' in d:
                pattern = d['projectKeyPattern']
        ptlist[name] = pattern
    return ptlist


# Method to get users from admin groups based on the name from Permission Template
def getAdmins(ptnames):
    members = {}
    for key, value in ptnames.items():
        users = []
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get("https://" + SQ_env + "/api/user_groups/users?name=" + key, headers=headers, verify=False)
        data = json.loads(response.text)

        for d in data['users']:
            users.append(d['login'])

        members[key] = users

    return members


# Method to get total number of pages
def getPages():
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.get("https://" + SQ_env + "/api/projects/search", headers=headers, verify=False)
    data = json.loads(response.text)
    pages = (data['paging']['total']/data['paging']['pageSize'])
    pages = math.ceil(pages)
    total = data['paging']['total']
    return pages, total


# Method to get project details and generate a csv report
def getData(ptnames, members):
    pages, total = getPages()
    # print("Total projects: ", total)
    file = open("SonarQubeLastAnalysis.csv", "a")
    file.write("Name, Key, Last Analysis Date, Owners\n")
    for p in range(1, pages+1):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.get("https://" + SQ_env + "/api/projects/search?p=" + str(p), headers=headers, verify=False)
        data = json.loads(response.text)
        for d in (data['components']):
            name = d['name']
            prjkey = d['key']
            if 'lastAnalysisDate' in d:
                lastAnalysisDate = d['lastAnalysisDate']
            else:
                lastAnalysisDate = "Null"
            for k, v in ptnames.items():
                if re.search(v, d['key']):
                    group = k
                    break
                else:
                    group = "NULL"
            if group == "NULL":
                admins = "No Owners"
            else:
                admins = members[group]
                admins = str(admins)
                admins = admins.replace(",", ";")
            file.write(name + ", " + prjkey + ", " + lastAnalysisDate + ", " + admins + "\n")
    file.close()


# Method calls
ptnames = getptData()
members = getAdmins(ptnames)
getData(ptnames, members)
