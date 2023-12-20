from api import *

def main():
    api = API()
    api.login()
    absences = api.get_all_absences()
    print(absences)
    
    # print(api.getAbsencesBySemester(3))
    
    # print(api.getAbsencesBySemester(2))

    # print(api.getAbsencesBySemester(1))
    
if __name__ == "__main__":
    main()
