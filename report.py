#!/usr/bin/env python3

import csv
import sys
from collections import defaultdict, namedtuple
from typing import List, Dict

INPUT_FILE_NAME = 'Corp_Summary.csv'
DELIMITER = ';'

FULL_NAME_FIELD = 'ФИО полностью'
DEPARTMENT_FIELD = 'Департамент'
TEAM_FIELD = 'Отдел'
POSITION_FIELD = 'Должность'
RATING_FIELD = 'Оценка'
SALARY_FIELD = 'Оклад'
REQUIRED_FIELDS = {FULL_NAME_FIELD: str, DEPARTMENT_FIELD: str,
                   TEAM_FIELD: str, RATING_FIELD: float, SALARY_FIELD: int}

OUTPUT_FILE_NAME = 'Departments_Summary.csv'
DepartmentSummary = namedtuple('DepartmentSummary',
                               ['name', 'headcount', 'min_salary',
                                'max_salary', 'avg_salary'])


def read_input_file(file_name: str = INPUT_FILE_NAME):
    """
    Parses the input csv file. Returns the list of rows, each row represents a
    parsed employee record. Similarly to the format used by DictReader each row
    is a dict, another option would be to use e.g. namedtuple, we use dict
    for the sake of simplicity.
    """
    with open(file_name, mode='r', newline='') as input_file:
        reader = csv.DictReader(input_file, delimiter=DELIMITER)
        return [{field: value(row[field]) for field, value in
                 REQUIRED_FIELDS.items()} for row in reader]


def print_company_hierarchy(rows: List[Dict]):
    """
    Prints the company hierarchy, i.e. the teams grouped by their departments.
    """
    departments = defaultdict(set)
    for row in rows:
        departments[row[DEPARTMENT_FIELD]].add(row[TEAM_FIELD])
    for department_name, teams in departments.items():
        print(department_name)
        for team in teams:
            print(f"  {team}")


def build_department_summaries(rows: List[Dict]):
    """
    Returns the department summaries, i.e. for each department calculates
    the headcount and the min, max, avg salary values.
    """
    salaries_by_department = defaultdict(list)
    for row in rows:
        salaries_by_department[row[DEPARTMENT_FIELD]].append(row[SALARY_FIELD])
    return [DepartmentSummary(name=department_name, headcount=len(salaries),
                              min_salary=min(salaries),
                              max_salary=max(salaries),
                              avg_salary=sum(salaries) / len(salaries)) for
            department_name, salaries in salaries_by_department.items()]


def print_department_summaries(summaries: List[DepartmentSummary]):
    """
    Prints the department summaries in a human readable format.
    """
    for summary in summaries:
        print(f"{summary.name}: headcount: {summary.headcount}, "
              f"min: {summary.min_salary}, max: {summary.max_salary}, "
              f"avg: {summary.avg_salary:.1f}")


def write_department_summaries(summaries: List[DepartmentSummary],
                               file_name: str = OUTPUT_FILE_NAME):
    """
    Writes the department summaries in the csv format
    ('name', 'headcount', 'min_salary', 'max_salary', 'avg_salary')
    into the specified output file.
    """
    with open(file_name, mode='w', newline='') as output_file:
        writer = csv.DictWriter(output_file,
                                fieldnames=DepartmentSummary._fields)
        writer.writeheader()
        writer.writerows((summary._asdict() for summary in summaries))


def main():
    while True:
        print("\nPlease, choose one of the available options: \n"
              "to print the teams hierarchy, type '1'\n"
              "to print the summary of all departments, type '2'\n"
              "to save the summary into 'Departments_Summary.csv', type  '3'\n"
              "quit, type 'q'\n")
        option = input()
        if option == 'q':
            sys.exit(0)
        elif option == '1':
            rows = read_input_file()
            print_company_hierarchy(rows)
        elif option == '2':
            rows = read_input_file()
            print_department_summaries(build_department_summaries(rows))
        elif option == '3':
            rows = read_input_file()
            write_department_summaries(build_department_summaries(rows))


if __name__ == '__main__':
    main()
