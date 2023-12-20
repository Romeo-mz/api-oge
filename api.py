import re
import requests
from bs4 import BeautifulSoup
import os

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
        
    def get_user(self):
        user = self.username
        return user
    
    def login_callback(self):
        login_callback_url = "https://casiut21.u-bourgogne.fr/cas-esirem/login?service=http%3A%2F%2F127.0.0.1%3A5000%2Fcallback"
        response = self.session.get(login_callback_url)

    def get_absences_page(self):
        print("Get absences page...")
        response = self.session.get(self.absences_url)
        return response.text

    def check_login(self, username, password):
        self.username = username
        self.password = password
        return self.login()

    def get_grades_page(self):
        print("Get grades page...")
        response = self.session.get(self.grades_url)
        return response.text

    def get_absences_by_semester(self, semester):
        absences_page = self.select_absences_semester(semester)
        soup = BeautifulSoup(absences_page, 'html.parser')

        absences_table = soup.find_all('tr', class_='ui-widget-content')
        print(f"Found {len(absences_table)} absences")

        absences = []
        for row in absences_table:
            columns = row.find_all('td', class_='ui-panelgrid-cell')
            absence_data = [column.get_text(strip=True) for column in columns]
            absences.append(absence_data)

        return absences

    def get_all_absences(self):
        all_absences = []
        min_semester = self.get_min_semester()
        max_semester = self.get_max_semester()
        total_semesters = max_semester - min_semester + 1
        print("Get all absences...")
        print(f"Found {total_semesters} semesters")
        for semester in range(total_semesters, 0, -1):
            absences = self.get_absences_by_semester(semester)
            all_absences.append(absences)
        return all_absences

    def get_min_semester(self):
        absences_page = self.get_absences_page()

        soup = BeautifulSoup(absences_page, 'html.parser')
        min_semester_text = soup.find('span', class_='ui-menuitem-text').get_text()

        min_semester = int(min_semester_text.split()[-1])
        return min_semester

    def get_max_semester(self):
        absences_page = self.get_absences_page()
        soup = BeautifulSoup(absences_page, 'html.parser')

        semesters = soup.find_all('span', class_='ui-menuitem-text')
        highest_semester = 0

        for semester in semesters:
            semester_text = semester.get_text()
            semester_number = int(semester_text.split(' ')[-1].split('Semestre')[-1])
            highest_semester = max(highest_semester, semester_number)

        return highest_semester if highest_semester > 0 else "No semesters found"

    def get_current_study_year(self):
        absences_page = self.get_absences_page()
        soup = BeautifulSoup(absences_page, 'html.parser')

        span_elements = soup.find_all('span', class_='ui-menuitem-text')
        highest_year = 0

        for span in span_elements:
            text = span.get_text()
            year = int(text.split(' ')[0][0]) if any(s in text for s in ['1A', '2A', '3A', '4A', '5A']) else 0
            highest_year = max(highest_year, year)

        return f"{highest_year}A" if highest_year > 0 else "No year found"

    def get_grades(self, semester):
        grades_page = self.select_grades_semester(semester)

        soup = BeautifulSoup(grades_page, 'html.parser')

        # To do later...

        grades = []

        return grades

    def select_absences_semester(self, semester):
        headers = {
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        data = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": f"ficheEtudiantForm:j_id_16_{semester}",
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "ficheEtudiantForm:panel",
            f"ficheEtudiantForm:j_id_16_{semester}": "ficheEtudiantForm:j_id_16_2",
            "ficheEtudiantForm_SUBMIT": "1",
            "javax.faces.ViewState": "0"
        }

        # Send the request
        response = self.session.post(self.absences_url, headers=headers, data=data)

        # Process the response to extract the real content
        content = response.text.split("![CDATA[")[1].split("]]")[0]

        return content

    def select_grades_semester(self, semester):
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