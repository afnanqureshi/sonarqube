'''
    This script generates a document that
    mentions the plugins installed in SonarQube.
    __author__ = "Mohd Afnan Qureshi"
    __maintainer__ = "Mohd Afnan Qureshi"
    __email__ = "md.afnan1995@gmail.com"
    __status__ = "Production"
'''


# Imports
import requests
import json
import os
from urllib3.exceptions import InsecureRequestWarning


# Global variable declaration
url = "https://sonarqube.com/"
token = os.getenv('token')
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + token
}


# Function to get plugin data
def get_data():
    name = []
    version = []
    urls = []
    description = []
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.get(url + "api/plugins/installed", headers=headers, verify=False)
    data = json.loads(response.text)
    data = data['plugins']
    for d in data:
        if 'homepageUrl' in d:
            name.append(d['name'])
            version.append(d['version'])
            urls.append(d['homepageUrl'])
            description.append(d['description'])
        else:
            name.append(d['name'])
            version.append(d['version'])
            urls.append('http://www.sonarsource.com')
            description.append(d['description'])
    print_data(name, version, urls, description)


# Function to generate the .md file
def print_data(name, version, urls, description):
    file = open("SonarQubePlugins.md", "a")
    file.write("# SonarQube : Plugins Installed"
               "\n\nList of plugins currently installed in SonarQube:\n\n| Plugins | Description | Version"
               " | More Info |\n| ----- | ----- | ----- | ----- |\n")
    for i in range(len(name)):
        file.write("| ")
        file.write(name[i]);
        file.write(" | ")
        file.write(description[i]);
        file.write(" | ")
        file.write(version[i]);
        file.write(" | [SonarSource](")
        file.write(urls[i]);
        file.write(") |\n")
    file.close()


# Function calls
get_data()
