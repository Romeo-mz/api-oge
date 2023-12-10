from api import API

def format_absence_data(absences):
    formatted_absences = []
    # TO do

def main():
    api = API()
    api.login()
    absences = api.getAllAbsences()

    formatted_absences = format_absence_data(absences)

    for entry in formatted_absences:
        print(entry)

if __name__ == "__main__":
    main()
