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

                    # Check if entry has enough elements before accessing them
                    if len(entry) >= 4:
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
                    else:
                        # Handle cases where the entry doesn't have enough elements
                        print("Entry doesn't have enough elements:", entry)

    process_absence(absences)
    return formatted_absences

def extract_subject(course):
    # Split the course name by common separators to extract the subject
    separators = ['_', '-', ':', ' ']
    for separator in separators:
        if separator in course:
            return course.split(separator)[0].strip()
    return course 

def extract_hours(date_time):
    # Date time date_time': 'Le 03/04/2023 de 08:15 à 10:00'
    start_time = date_time.split('de')[1].split('à')[0].strip()
    end_time = date_time.split('à')[1].strip()
    total_hours = int(end_time.split(':')[0]) - int(start_time.split(':')[0])
    return total_hours

def absences_by_course(absences):
    absences_by_course = {}
    
    for absence in absences:
        course = absence['course']
        subject = extract_subject(course)
        hours_by_absence = extract_hours(absence['date_time'])
        if subject in absences_by_course:
            
            absences_by_course[subject] += hours_by_absence
        else:

            absences_by_course[subject] = hours_by_absence
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
