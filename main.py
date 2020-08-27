import tabula as tab
import wget
import os
import pandas as pd
import itertools

class aula:
    def __init__(self, course):
        self.course = course
        self.time = []

    def add_time(self, time):
        self.time.append(time)

    def print(self):
        print("############# AULA DE", self.course, "################")
        for time in self.time:
            print("Turno:", time[1])
            print("Horário:", time[0])

def download_file(link):
    filename = wget.download(link)
    if not filename.endswith('.pdf'):
        print(filename, "does not end with .pdf")
        os.system("mv " + filename + " " + filename + ".pdf")
        filename += '.pdf'
    return filename

def pdf_to_csv(input_file, output_file='schedule.csv'):
    tab.convert_into(input_file, output_file, output_format='csv', pages='all')
    return output_file

def read_csv(filename):
    return pd.read_csv(filename)

def filter_schedule(full_schedule, courses, semester):
    filtered_for_courses = full_schedule[full_schedule['Unidades Curriculares'].isin(courses)]
    filtered_for_courses = filtered_for_courses[filtered_for_courses['Semestre'] == semester]
    return filtered_for_courses.reset_index(drop=True)

'''
TODO consider that the first TP is not always 1
'''
def generate_groups_for_combinations(schedule):
    courses_block = []
    current_course = ''
    i = 0
    double_shift = None
    while True:
        if i == len(schedule.values):
            break
        current_course = schedule['Unidades Curriculares'][i]
        tp = 1
        new_class = aula(current_course)
        course = []
        while i < len(schedule.values) and schedule['Unidades Curriculares'][i] == current_course:
            if not 'TP' + str(tp) in schedule['Turno'][i]:
                tp += 1
                course.append(new_class)
                new_class = aula(current_course)
                if double_shift and "TP" + str(tp) in double_shift[1]:
                    new_class.add_time(double_shift)
                    double_shift = None
            new_time = [generate_time(schedule, i), schedule['Turno'][i]]
            new_class.add_time(new_time)
            if schedule['Turno'][i].count("TP") > 1:
                double_shift = new_time
            i += 1
        course.append(new_class)
        courses_block.append(course)
    return courses_block

def generate_time(schedule, line):
    time = {}
    time['2.a'] = schedule['2.a'][line]
    time['3.a'] = schedule['3.a'][line]
    time['4.a'] = schedule['4.a'][line]
    time['5.a'] = schedule['5.a'][line]
    time['6.a'] = schedule['6.a'][line]
    time['Sáb'] = schedule['Sáb'][line]
    
    return time

def generate_all_schedules(courses_schedules):
    return list(itertools.product(*courses_schedules))

link = 'https://www.letras.ulisboa.pt/pt/documentos/cursos/-1/6781--2702/file'
courses = ['Inglês Vantagem Avançado (B2.2)', 'Cultura Clássica']
semester = 'S1'

##############################################################
########## TEMP ZONE - GET DIFFERENT TABLE READER ############
##############################################################

filename = 'Horarios-Licenciaturas-2020-2021-v07.pdf' #download_file(link)
#csv_file = pdf_to_csv(filename)

full_schedule = read_csv('schedule.csv')
filtered_schedule = filter_schedule(full_schedule, courses, semester)

classes = generate_groups_for_combinations(filtered_schedule)

full_list_schedules = generate_all_schedules(classes)

# TODO Filter full_list_schedules to remove impossible ones

##############################################################
###################### END TEMP ZONE #########################
##############################################################


def main():
    filename = download_file(link)
    csv_file = pdf_to_csv(filename)
    full_schedule = read_csv(csv_file)
    filtered_schedule = filter_schedule(full_schedule, courses, semester)
    classes = generate_groups_for_combinations(filtered_schedule)

    # Insert here full list of schedules
    schedules = []

    return schedules