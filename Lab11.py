import matplotlib.pyplot as plt

import os

def display_menu():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    print()

def students_file():
    students = {}
    with open('data/students.txt','r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        stu_id = line[:3]
        name = line[3:].strip()
        students[name.lower()] = stu_id

    return students

def assignment_file():
    assignments = {}
    with open('data/assignments.txt','r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]

    for i in range(0, len(lines), 3):
        name = lines[i]
        id_num = lines[i + 1]
        points = int(lines[i + 2])
        assignments[id_num] = {"name": name, "points": points}

    return assignments

def submission_folder():
    submissions = {}
    folder = 'data/submissions'

    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                stu_id, id_num, percent = line.split('|')
                percent = float(percent)

                if stu_id not in submissions:
                    submissions[stu_id] = {}
                submissions[stu_id][id_num] = percent
    return submissions

def stu_grade(students, name, assignments, submissions):
    stu_id = students.get(name.lower())
    if not stu_id:
        return None

    total = sum(i["points"] for i in assignments.values())

    new = 0
    for id_num, i in assignments.items():
        points = i["points"]
        percent = submissions[stu_id][id_num]
        new += points * (percent/100)

    percent_grade = round((new / total) * 100)
    return percent_grade

def assignment_stats(assignments, submissions):
    name = input("What is the assignment name: ").strip()
    id_num = None
    for nid, i in assignments.items():
        if i["name"].lower() == name.lower():
            id_num = nid
            break
    if id_num is None:
        print("Assignment not found")
        return

    scores = []
    for s in submissions.values():
        if id_num in s:
            scores.append(s[id_num])

    maxi = round(max(scores))
    mini = round(min(scores))
    avg = int(sum(scores) / len(scores))

    print(f"Min: {mini}%")
    print(f"Avg: {avg}%")
    print(f"Max: {maxi}%")

def graph(assignments, submissions):
    name = input("What is the assignment name: ").strip()
    id_num = None
    for nid, i in assignments.items():
        if i["name"].lower() == name.lower():
            id_num = nid
            break
    if id_num is None:
        print("Assignment not found")
        return

    scores = []
    for s in submissions.values():
        if id_num in s:
            scores.append(s[id_num])

    plt.hist(scores, bins=[50,55,60,65,70,75,80,85,90,95,100])
    plt.show()

def main():
    students = students_file()
    assignments = assignment_file()
    submissions = submission_folder()
    display_menu()
    option = int(input("Enter your selection: "))

    if option == 1:
        name = input("What is the student's name: ")
        grade = stu_grade(students,  name, assignments, submissions)
        if grade is None:
            print("Student not found")
        else:
            print(f"{grade}%")

    elif option == 2:
        assignment_stats(assignments, submissions)

    elif option == 3:
        graph(assignments, submissions)




if __name__ == '__main__':
    main()
