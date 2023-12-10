from api import API

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
     
def main():
    api = API()
    api.login()
    absences = api.getAllAbsences()

    formatted_absences = format_absence_data(absences)

    for entry in formatted_absences:
        print(entry)

if __name__ == "__main__":
    main()
