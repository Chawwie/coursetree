import json
import re   

CourseCodePattern = re.compile("([A-Z]{4}[0-9]{4})")

def courseExists(courses, id):
    for course in courses:
        if course['id'] == id:
            return True
    return False

def addCourse(courses, id):
    courses.append({
        "id": id,
        "parentIds": []
    })

def deleteCourse(courses, id):
    for course in courses:
        if course['id'] == id:
            courses.remove(course)
        elif id in course['parentIds']:
            course['parentIds'].remove(id)

# Attaches all courses without parents to a ROOT node
def adoptOphans(courses):
    for course in courses:
        if len(course['parentIds']) == 0:
            course['parentIds'].append('ROOT')

    # Create root node if doesn't exist yet
    if not courseExists(courses, 'ROOT'):
        addCourse(courses, 'ROOT')

def removeImmediateCycles(courses):
    for course in courses:
        if course['id'] in course['parentIds']:
            course['parentIds'].remove(course['id'])

def deleteObsoleteCourses(courses):
    obsoleteCourses = []
    for course in courses:
        if 'obsolete' in course and course['obsolete']:
            obsoleteCourses.append(course['id'])
    for course in obsoleteCourses:
        deleteCourse(courses, course)


with open('./courses/courses.json', 'r') as f:
    courses = json.load(f);
    for course in courses:
        # Parse course code for current course
        course['id'] = CourseCodePattern.search(course['name']).group(1)
        del course['name']

        # Parse prerequisite coure codes
        course['parentIds'] = []
        if course['pre'] is not None:
            prereqs = course['pre']
            prereqCodes = CourseCodePattern.findall(prereqs) 
            # if not prereqCodes and prereqs == "Permission of Head of School":
                # course['headpermission'] = True
            course['parentIds'] = prereqCodes
        del course['pre']
            
    # add missing courses
    for course in courses:
        for prereq in course['parentIds']:
            if not courseExists(courses, prereq):
                addCourse(courses, prereq)
    # ROOT the dag
    adoptOphans(courses)
    
    removeImmediateCycles(courses)

    deleteObsoleteCourses(courses)

    # Final Output
    fout = open('uq.json', 'w')
    json.dump(courses, fout, indent=2)
