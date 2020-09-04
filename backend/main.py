import tabula as tab
import wget
import os
import pandas as pd
import itertools
import re
import math
import json

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

    def to_frontend_time(self, day, time):
        weekday_to_frontend = {
            '2.a': '2020-08-31',
            '3.a': '2020-09-01',
            '4.a': '2020-09-02',
            '5.a': '2020-09-03',
            '6.a': '2020-09-04',
            'Sáb': '2020-09-05',
        }

        return "{} {}:00".format(weekday_to_frontend[day], time) 

    def time_to_jsons(self, time):
        to_return = []
        for day in time[0]:
            # Ignores nan (NotANumber)
            if type(time[0][day]) != float:
                to_return += [{
                    'name':  self.course + " (" + time[1] + ")",
                    'start': self.to_frontend_time(day, time[0][day].split('-')[0]),
                    'end':   self.to_frontend_time(day, time[0][day].split('-')[1]),
                    'color': 'red' 
                }]
        return to_return

    def to_json(self):
        to_return = []
        for time in self.time:
            to_return += self.time_to_jsons(time)
        return to_return

def download_file(link):
    filename = wget.download(link)
    if not filename.endswith('.pdf'):
        print(filename, "does not end with .pdf")
        os.system("mv " + filename + " " + filename + ".pdf")
        filename += '.pdf'
    return filename

def pdf_to_csv(input_file, output_file='csv/schedule.csv'):
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

def is_possible(schedule):
    mounted_schedule = {'2.a': [], '3.a': [], '4.a': [], '5.a': [], '6.a': [], 'Sáb': []}

    for course in schedule:
        time = course.time 
        for shift in time:
            for day in shift[0]:
                if type(shift[0][day]) != float and has_colision(shift[0][day], mounted_schedule[day]):
                    return False
                mounted_schedule[day] += [shift[0][day]]
    return True

def has_colision(new, occupied):
    if occupied == []:
        return False
    [start, end] = new.split('-')
    for filled in occupied:
        if type(filled) == float and math.isnan(filled):
            continue
        [filled_start, filled_end] = filled.split('-')
        if start >= filled_start and start < filled_end:
            return True
        elif end > filled_start and end <= filled_end:
            return True
        elif start < filled_start and end > filled_end:
            return True
    return False


def remove_impossible_schedules(schedules):
    return [schedule for schedule in schedules if is_possible(schedule)]

def schedules_to_json(schedules):
    new_schedules = {}
    i = 0
    for schedule in schedules:
        new_schedules[i] = []
        for shift in schedule:
            new_schedules[i] += shift.to_json()
        i += 1

    return json.dumps(new_schedules)

link = 'https://www.letras.ulisboa.pt/pt/documentos/cursos/-1/6781--2702/file'
courses = ['Inglês Vantagem Avançado (B2.2)', 'Cultura Clássica']
semester = 'S1'


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

def temp_main(temp_courses):
    full_schedule = read_csv('csv/schedule.csv')
    filtered_schedule = filter_schedule(full_schedule, temp_courses, semester)

    classes = generate_groups_for_combinations(filtered_schedule)
    classes = split_bifurcated_classes(classes)
    full_list_schedules = generate_all_schedules(classes)
    schedules = remove_impossible_schedules(full_list_schedules)
    schedules = schedules_to_json(schedules)
    return schedules
