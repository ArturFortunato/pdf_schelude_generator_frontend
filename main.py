import tabula as tab
import wget
import os
import pandas as pd
import itertools
import re

class turno:
    def __init__(self, course):
        self.course = course
        self.time = []

    def add_time(self, time):
        self.time.append(time)

    def print(self):
        print("############# TURMA DE", self.course, "################")
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
        new_class = turno(current_course)
        course = []
        while i < len(schedule.values) and schedule['Unidades Curriculares'][i] == current_course:
            if not 'TP' + str(tp) in schedule['Turno'][i]:
                tp += 1
                course.append(new_class)
                new_class = turno(current_course)
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

def split_bifurcated_classes(schedule):
    course_index = 0
    for course in schedule:
        to_remove = {}
        current_course = None
        for i in range(len(course)):
            current_course = course[i].course
            for time in course[i].time:
                if re.search("TP[\d]*[A-Z]", time[1]):
                    if i in to_remove:
                        to_remove[i] += 1
                    else:
                        to_remove[i] = 1

        course += generate_splited(course, to_remove, current_course)
        schedule[course_index] = [course[i] for i in range(len(course)) if i not in to_remove]
        course_index += 1
    return schedule

def generate_splited(course, to_change, current_course):
    new_shifts = []
    for turma in to_change:
        current = 0
        splited_classes = []
        for i in range(to_change[turma]):
            splited_classes += [turno(current_course)]
        for horario_turma in course[turma].time:
            tp_id = get_after_digits(horario_turma[1])
            if horario_turma[1][tp_id].isalpha():
                splited_classes[current].add_time(horario_turma)
                current += 1
            else:
                for i in range(len(splited_classes)):
                    splited_classes[i].add_time(horario_turma)
        new_shifts += splited_classes

    return new_shifts

def get_after_digits(class_name):
    base = class_name.index("TP") + 3
    while class_name[base].isdigit():
        base += 1
    return base

def generate_all_schedules(courses_schedules):
    return list(itertools.product(*courses_schedules))

def remove_impossible_schedules(schedules):
    # TODO
    return schedules

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
classes = split_bifurcated_classes(classes)
full_list_schedules = generate_all_schedules(classes)
schedules = remove_impossible_schedules(full_list_schedules)


##############################################################
###################### END TEMP ZONE #########################
##############################################################


def main():
    # Get PDF file
    filename = download_file(link)

    # Convert PDF table to CSV
    csv_file = pdf_to_csv(filename)

    # Get Full college schedule
    full_schedule = read_csv(csv_file)

    # Get schedule for all the student's classes 
    filtered_schedule = filter_schedule(full_schedule, courses, semester)

    # Organize schedules for each course
    classes = generate_groups_for_combinations(filtered_schedule)

    # Split shifts that are double (like TP1+TP1A and TP1+TP1B)
    classes = split_bifurcated_classes(classes)

    # Generate all combinations
    full_list_schedules = generate_all_schedules(classes)
    
    # Remove impossible schedules
    schedules = remove_impossible_schedules(full_list_schedules)

    return schedules