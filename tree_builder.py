import json
import re

def find(node, target):
    if node is None:
        return None;
    if node['name'] == target:
        return node
    found = false

    

with open('./courses/courses.json', 'r') as f:
    
    data = json.load(f);
    courseList = {}
    nodes = []
    links = []

    # Parse prerequisites
    courseCodePattern = re.compile("([A-Z]{4}[0-9]{4})")
    for x in data:
        x['id'] = courseCodePattern.search(x['name']).group(1)
        courseList[(x['id'])] = "asdf"

        if x['pre'] is not None:
            courseCodes = courseCodePattern.findall(x['pre']) 
            if not courseCodes and x['pre'] == "Permission of Head of School":
                x['headpermission'] = True
            x['pre'] = courseCodes
            
    
    # Normalize data
    for x in data:
        if x['pre'] is None:
            x['pre'] = []

    # Create Nodes and Links
    for x in data:
        nodes.append({ 'id': x['id'], 'name': x['name']})
        for course in x['pre']:
            if course is not None and course in courseList:
                links.append({'source': x['id'], 'target': course})

    fout = open('uq.json', 'w')
    json.dump({'nodes': nodes, 'links': links}, fout, indent=2)
