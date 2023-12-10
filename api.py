import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

class API:
    def __init__(self, user=os.getenv("API_USERNAME"), pwd=os.getenv("API_PASSWORD")):
        self.username = user
        self.password = pwd
        self.home_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/"
        self.login_url = "https://casiut21.u-bourgogne.fr/cas-esirem/login?service=https%3A%2F%2Fiutdijon.u-bourgogne.fr%2Foge-esirem%2F"
        self.absences_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/absencesEtu.xhtml"
        self.grades_url = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/bilanEtu.xhtml"
        self.session = requests.Session()

        print(f"API created with username {self.username} and password {self.password}")

    def get(self, url):
        print(f"Get {url}")
        return self.session.get(url)

    def login(self):
        response = self.session.get(self.login_url)
        execution = re.search(r'name="execution" value="([^"]+)"', response.text).group(1)
        payload = {
            'username': self.username,
            'password': self.password,
            'execution': execution,
            '_eventId': 'submit'
        }
        login_response = self.session.post(self.login_url, data=payload)

        if "Connexion - CAS" not in login_response.text:
            print("Login successful")
            return True
        else:
            print("Login failed")
            return False

    def getAbsencesPage(self):
        print("Get absences page...")
        response = self.session.get(self.absences_url)
        return response.text
    
    def getGradesPage(self):
        print("Get grades page...")
        response = self.session.get(self.grades_url)
        return response.text
    
    def getAbsencesBySemester(self, semester):
        absencesPage = self.selectAbsencesSemester(semester)

        soup = BeautifulSoup(absencesPage, 'html.parser')

        absences_table = soup.find_all('tr', class_='ui-widget-content')
        print(f"Found {len(absences_table)} absences")

        absences = []
        for row in absences_table:
            columns = row.find_all('td', class_='ui-panelgrid-cell')
            absence_data = [column.get_text(strip=True) for column in columns]
            absences.append(absence_data)

        return absences

    def getAllAbsences(self):
        all_absences = []
        min_semester = self.getMinSemester()
        max_semester = self.getMaxSemester()
        total_semesters = max_semester - min_semester + 1
        print(f"Found {total_semesters} semesters")
        for semester in range(1, total_semesters + 1):
            absences = self.getAbsencesBySemester(semester)
            all_absences.append(absences)
        return all_absences
        
    def getMinSemester(self):
        absencesPage = self.getAbsencesPage()

        soup = BeautifulSoup(absencesPage, 'html.parser')
        min_semester_text = soup.find('span', class_='ui-menuitem-text').get_text()

        min_semester = int(min_semester_text.split()[-1])
        return min_semester

    def getMaxSemester(self):
        absencesPage = self.getAbsencesPage()
        soup = BeautifulSoup(absencesPage, 'html.parser')
        
        semesters = soup.find_all('span', class_='ui-menuitem-text')
        highest_semester = 0
        
        for semester in semesters:
            semester_text = semester.get_text()
            semester_number = int(semester_text.split(' ')[-1].split('Semestre')[-1])
            highest_semester = max(highest_semester, semester_number)

        return highest_semester if highest_semester > 0 else "No semesters found"

    def getCurrentStudyYear(self):
        absencesPage = self.getAbsencesPage()
        soup = BeautifulSoup(absencesPage, 'html.parser')
        
        span_elements = soup.find_all('span', class_='ui-menuitem-text')
        highest_year = 0
        
        for span in span_elements:
            text = span.get_text()
            year = int(text.split(' ')[0][0]) if any(s in text for s in ['1A', '2A', '3A', '4A', '5A']) else 0
            highest_year = max(highest_year, year)

        return f"{highest_year}A" if highest_year > 0 else "No year found"


    
    def getGrades(self, semester):
        gradesPage = self.selectGradesSemester(semester)

        soup = BeautifulSoup(gradesPage, 'html.parser')

        # To do later...

        grades = []

        return grades

    def selectAbsencesSemester(self, semester):
        headers = {
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        data = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "ficheEtudiantForm:j_id_16_" + str(semester),
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "ficheEtudiantForm:panel",
            "ficheEtudiantForm:j_id_16_" + str(semester): "ficheEtudiantForm:j_id_16_2",
            "ficheEtudiantForm_SUBMIT": "1",
            "javax.faces.ViewState": "0"
        }

        # Send the request
        response = self.session.post(self.absences_url, headers=headers, data=data)

        # Process the response to extract the real content
        content = response.text.split("![CDATA[")[1].split("]]")[0]

        return content

    def selectGradesSemester(self, semester):
        headers = {
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        data = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "mainBilanForm:j_id_15",
            "javax.faces.partial.execute": "mainBilanForm:j_id_15",
            "javax.faces.partial.render": "mainBilanForm",
            "mainBilanForm:j_id_15": "mainBilanForm:j_id_15",
            "i": str(int(semester) - 1),
            "mainBilanForm:j_id_15_menuid": str(int(semester) - 1),
            "mainBilanForm_SUBMIT": "1",
            "javax.faces.ViewState": "0"
        }

        # Send the request
        response = self.session.post(self.grades_url, headers=headers, data=data)

        # Process the response to extract the real content
        content = response.text.split("![CDATA[")[1].split("]]")[0]

        return content
