from pathlib import Path
import pandas as pd
from datetime import date

# main3.py is located directly inside the member3 folder
BASE_DIR = Path(__file__).resolve().parent

print("MAIN3 LOCATION:", __file__)
print("BASE_DIR:", BASE_DIR)

# CSV files are directly inside member3
tasks_file = BASE_DIR / "tasks.csv"
availability_file = BASE_DIR / "availability.csv"

print("TASK FILE:", tasks_file)
print("TASK FILE EXISTS:", tasks_file.exists())

print("AVAILABILITY FILE:", availability_file)
print("AVAILABILITY FILE EXISTS:", availability_file.exists())

tasks = pd.read_csv(tasks_file)
availability = pd.read_csv(availability_file)

from workload import calculate_workload
from prioritization import calculate_priority
from study_planner import generate_study_plan


# DISPLAY INPUT DATA


print("       UNIFLOW AI STUDY PLANNER          ")


print("\nTASKS:")
print(tasks)

print("\nAVAILABLE STUDY HOURS:")
print(availability)


# CALCULATE WORKLOAD


workload = calculate_workload(tasks)

print("          WORKLOAD ANALYSIS           ")


print("Total tasks:", workload["total_tasks"])
print("Total study hours required:", workload["total_hours"])
print("Average difficulty:", workload["average_difficulty"])
print("Workload level:", workload["workload_level"])


# CALCULATE TASK PRIORITIES


today = date(2026, 9, 21)

tasks["priority"] = tasks.apply(
    lambda row: calculate_priority(row, today),
    axis=1
)


# Sort highest priority first
tasks = tasks.sort_values(
    by="priority",
    ascending=False
)


print("             TASK PRIORITY")

print(
    tasks[
        [
            "task_name",
            "course",
            "difficulty",
            "required_hours",
            "deadline",
            "priority"
        ]
    ].to_string(index=False)
)


# GENERATE STUDY PLAN


study_plan, remaining_hours = generate_study_plan(
    tasks,
    availability,
    today
)


print("          GENERATED STUDY PLAN             ")


current_day = ""

for item in study_plan:

    if item["day"] != current_day:

        current_day = item["day"]

        print(f"\n{current_day} ({item['date']})")
        print("-" * 30)

    print(
        f'{item["task"]} '
        f'({item["course"]}) - '
        f'{item["hours"]} hour(s)'
    )


# CHECK FOR UNFINISHED TASKS


unfinished_tasks = {
    task: hours
    for task, hours in remaining_hours.items()
    if hours > 0
}


if unfinished_tasks:

    
    print("               WARNING                ")

    print("Some tasks could not be fully scheduled:")

    for task, hours in unfinished_tasks.items():
        print(f"- {task}: {hours} hour(s) remaining")

else:

    print("\nAll tasks have been scheduled successfully!")