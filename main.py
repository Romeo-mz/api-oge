from api import *
from getpass import getpass

def main():
    api = API()
    api.login()
    absences_s2 = api.getAbsencesBySemester(50)
    print(absences_s2)

    # absences = api.getAllAbsences()
    # print(absences)


if __name__ == "__main__":
    main()
