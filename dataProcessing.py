from api import API
import json
def format_absence_data(absences):
    formatted_absences = []

    def process_absence(absence):
        for entry in absence:
            if entry:
                if isinstance(entry[0], list):
                    process_absence(entry)  # Recursively handle deeper levels
                else:
                    course_info = entry[0].split('\n')  # Split course info
                    if len(course_info) == 2:
                        course = course_info[0].strip()
                        professor = entry[1].strip()
                        date_time = entry[2].strip()
                        status = entry[3].strip()
                        formatted_absences.append({
                            'course': course,
                            'professor': professor,
                            'date_time': date_time,
                            'status': status
                        })

    process_absence(absences)
    return formatted_absences

def extract_subject(course):
    # Split the course name by common separators to extract the subject
    separators = ['_', '-', ':', ' ']
    for separator in separators:
        if separator in course:
            return course.split(separator)[0].strip()
    return course 

def absences_by_course(absences):
    absences_by_course = {}
    
    for absence in absences:
        course = absence['course']
        subject = extract_subject(course)
        
        if subject in absences_by_course:
            absences_by_course[subject] += 1
        else:
            absences_by_course[subject] = 1  
    result = [{'course': course, 'total': total} for course, total in absences_by_course.items()]
    json_result = json.dumps(result)
    return json_result



def main():
    api = API()
    api.login()
    absences = api.getAllAbsences()
    print(absences)
    formatted_absences = format_absence_data(absences)
    print(formatted_absences)
    absences_course = absences_by_course(formatted_absences)
    print(absences_course)

if __name__ == "__main__":
    main()
