
# Study Planner section


from datetime import date, timedelta
import csv


#   Load Student Information


def load_student(filename):

    with open(filename, "r") as file:

        reader = csv.DictReader(file)

        student_data = next(reader)

    return {
        "name": student_data["student_name"],
        "study_hours_per_day": int(
            student_data["study_hours_per_day"]
        ),
        "available_days": student_data[
            "available_days"
        ].split("|")
    }


 
#  Load Tasks
 

def load_tasks(filename):

    tasks = []

    with open(filename, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            tasks.append({
                "name": row["name"],
                "course": row["course"],
                "deadline": row["deadline"],
                "difficulty": row["difficulty"],
                "estimated_hours": int(
                    row["estimated_hours"]
                ),
                "priority": row["priority"],
                "remaining_hours": int(
                    row["estimated_hours"]
                )
            })

    return tasks



#   Difficulty Score
 

def difficulty_score(difficulty):

    if difficulty == "Hard":
        return 3

    elif difficulty == "Medium":
        return 2

    else:
        return 1


#   Priority Scores

def priority_score(priority):

    if priority == "High":
        return 3

    elif priority == "Medium":
        return 2

    else:
        return 1



#   Calculate Task Priority


def calculate_priority(tasks):

    today = date.today()

    for task in tasks:

        deadline = date.fromisoformat(
            task["deadline"]
        )

        task["days_remaining"] = (
            deadline - today
        ).days

        task["difficulty_score"] = (
            difficulty_score(
                task["difficulty"]
            )
        )

        # Deadline urgency

        if task["days_remaining"] <= 1:

            deadline_score = 3

        elif task["days_remaining"] <= 3:

            deadline_score = 2

        else:

            deadline_score = 1

        task["deadline_score"] = deadline_score

        # Final priority score

        task["priority_score"] = (
            deadline_score
            + task["difficulty_score"]
            + priority_score(
                task["priority"]
            )
        )

    tasks.sort(
        key=lambda task: (
            task["priority_score"],
            -task["days_remaining"]
        ),
        reverse=True
    )

    return tasks

#   Generate Study Plan


def generate_study_plan(
    tasks,
    available_days,
    study_hours_per_day
):

    today = date.today()

    plan = []

    for day_name in available_days:

        current_date = today

        # Find the next occurrence
        # of the selected weekday

        while current_date.strftime(
            "%A"
        ) != day_name:

            current_date += timedelta(days=1)

        remaining_day_hours = (
            study_hours_per_day
        )

        # Find tasks that can be scheduled

        available_tasks = []

        for task in tasks:

            if task["remaining_hours"] <= 0:
                continue

            deadline = date.fromisoformat(
                task["deadline"]
            )

            # Do not schedule after deadline

            if current_date > deadline:
                continue

            available_tasks.append(task)

        # Sort by priority

        available_tasks.sort(
            key=lambda task: (
                task["priority_score"],
                -task["remaining_hours"]
            ),
            reverse=True
        )

        # Allocate study hours

        for task in available_tasks:

            if remaining_day_hours <= 0:
                break

            hours_to_assign = min(
                task["remaining_hours"],
                remaining_day_hours
            )

            plan.append({
                "day": day_name,
                "date": current_date,
                "task": task["name"],
                "course": task["course"],
                "hours": hours_to_assign
            })

            task["remaining_hours"] -= (
                hours_to_assign
            )

            remaining_day_hours -= (
                hours_to_assign
            )

    return plan

#   Display Student Information


def display_student(student):

    print("===================================")
    print("       UNIFLOW AI STUDY PLANNER")
    print("===================================")

    print()

    print(
        "Student:",
        student["name"]
    )

    print(
        "Available Days:",
        student["available_days"]
    )

    print(
        "Study Hours Per Day:",
        student["study_hours_per_day"]
    )

#   Display Task Priority


def display_task_priority(tasks):

    print()
    print("      TASK PRIORITY    ")

    for task in tasks:

        print()

        print(
            "Task:",
            task["name"]
        )

        print(
            "Course:",
            task["course"]
        )

        print(
            "Deadline:",
            task["deadline"]
        )

        print(
            "Days Remaining:",
            task["days_remaining"]
        )

        print(
            "Difficulty:",
            task["difficulty"]
        )

        print(
            "Priority:",
            task["priority"]
        )

        print(
            "Priority Score:",
            task["priority_score"]
        )



#   Display Study Plan


def display_study_plan(plan):

    print()
    print("  GENERATED STUDY PLAN    ")

    current_day = None

    total_hours = 0

    for item in plan:

        if item["day"] != current_day:

            current_day = item["day"]

            print()
            print(
                item["day"],
                "(",
                item["date"],
                ")"
            )

            print("----------------")

        print(
            "-",
            item["task"],
            "(",
            item["course"],
            ")",
            "->",
            item["hours"],
            "hour(s)"
        )

        total_hours += item["hours"]

    print()
    print(
        "Total Scheduled Study Hours:",
        total_hours
    )


 
#   Display Task Status
 

def display_unfinished_tasks(tasks):

    print()
    print("====== TASK STATUS ======")

    today = date.today()

    unfinished_tasks = False

    for task in tasks:

        if task["remaining_hours"] > 0:

            unfinished_tasks = True

            deadline = date.fromisoformat(
                task["deadline"]
            )

            if deadline < today:

                print(
                    "-",
                    task["name"],
                    "-> OVERDUE",
                    "|",
                    task["remaining_hours"],
                    "hour(s) remaining"
                )

            else:

                print(
                    "-",
                    task["name"],
                    "-> NOT ENOUGH STUDY TIME",
                    "|",
                    task["remaining_hours"],
                    "hour(s) remaining",
                    "| Deadline:",
                    task["deadline"]
                )

    if not unfinished_tasks:

        print(
            "All tasks have been scheduled!"
        )
 
# Save Study Plan
 

def save_study_plan(plan, filename):

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        fieldnames = [
            "day",
            "date",
            "task",
            "course",
            "hours"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for item in plan:

            writer.writerow({
                "day": item["day"],
                "date": item["date"],
                "task": item["task"],
                "course": item["course"],
                "hours": item["hours"]
            })


 
#   Main 
 

def main():

    student = load_student(
        "student.csv"
    )

    tasks = load_tasks(
        "tasks.csv"
    )

    tasks = calculate_priority(
        tasks
    )

    display_student(
        student
    )

    display_task_priority(
        tasks
    )

    plan = generate_study_plan(
        tasks,
        student["available_days"],
        student["study_hours_per_day"]
    )

    display_study_plan(
        plan
    )

    save_study_plan(
        plan,
        "study_plan.csv"
    )

    display_unfinished_tasks(
        tasks
    )


 
#   Start Program
 

if __name__ == "__main__":

    main()