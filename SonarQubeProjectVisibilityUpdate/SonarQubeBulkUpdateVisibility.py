'''
    This python script bulk updates the visibility of selected projects in SonarQube.
    The steps to run the script are as follows:
    1. Set the environment in the 'SQ_env' variable in which the projects' visibility needs
        to be changed.
    2. Set the admin token in the 'SQ_token' variable.
    3. Set the 'visibility' variable to 'private' or 'public'
    4. Set the 'key_expression' variable to match the key pattern of those projects whose
        visibility needs to be changed.
    5. Run the script as a python file
    NOTE: The 'key_expression' variable here is a regular expression and not a string.
        For example: If the key_expression is set to '^example.com', it will change the
        visibility of all the projects that have a key pattern that starts with
         'example.com'.
        For projects that you want to just match the key pattern, end the key_expression with a
        '$' symbol. For example '^example.com.test$' will only update project that has a key
        pattern of 'example.com.test'
    __author__ = "Mohd Afnan Qureshi"
    __maintainer__ = "Mohd Afnan Qureshi"
    __email__ = "md.afnan1995@gmail.com"
    __status__ = "Production"
'''

# Imports
import json
import math
import re
import os


# Global Variable declaration
SQ_env = "sonarqube.com"         			                # The environment you want to update the projects on (dev/prod)
SQ_token = os.getenv('token') 								# The admin token
visibility = "private"                           			# The visibility you want to set (private/public)
key_expression = '^example.com.test'          		     	# The key expression to match the key pattern of the projects
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + SQ_token
}


# Function to get the total number of pages of API
def getPages (data):
    pages = (data['paging']['total']/data['paging']['pageSize'])
    pages = math.ceil(pages)
    return pages


# Function to search selected projects
def searchProjects(pages):
    projects = []
    for p in range(1, pages+1):
        file = str(p) + ".txt"
        data = json.load(open(file))
        for d in data['components']:
            if re.search(key_expression, d['key']):
                projects.append(d['key'])
    return projects


# Function to remove all the files after update
def removeFiles(pages):
    for p in range(1, pages+1):
        param = "rm " + str(p) + ".txt"
        os.system(param)
    os.system("rm sq_projects_list.txt")


# Function to get the API from environment
def getAPI ():
    param = "curl -o 1.txt -u " + SQ_token + ": http://" + SQ_env + "/api/projects/search"
    os.system(param)
    data = json.load(open('1.txt'))
    pages = getPages(data)
    if (pages>1):
        for p in range(2, pages+1):
            param = "curl -o " + str(p) + ".txt" + " -u " + SQ_token + ":" + " http://" + SQ_env + "/api/projects/search?p=" + str(p)
            os.system(param)
    return pages


# Function to update the visibility
def updateVisibility():
    with open('sq_projects_list.txt', 'r') as file:
        print("The following projects will be updated: ")
        while True:
            f = file.readline().rstrip('\n')
            if not f:
                break
            else:
                print(f)
    with open('sq_projects_list.txt', 'r') as file:
        ans = str(input("Do you want to continue? (Y/N) "))
        if ans == 'Y' or ans == 'y':
            while True:
                f = file.readline().rstrip('\n')
                if not f:
                    break
                else:
                    param = "curl -X POST -u " + SQ_token + ":" + " -X POST \"http://" + SQ_env + "/api/projects/update_visibility?project=" + f + "&visibility=" + visibility +"\""
                    os.system(param)
            print("The projects were successfully updated")
        else:
            print("The projects were not updated")


# Function to write searched projects to a file
def writeProjects(projects):
    with open('sq_projects_list.txt', 'w') as w:
        for i in range(0, len(projects)):
            w.write(projects[i])
            w.write('\n')


pages = getAPI()
projects = searchProjects(pages)
writeProjects(projects)
updateVisibility()
removeFiles(pages)
