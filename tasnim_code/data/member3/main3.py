from pathlib import Path
import pandas as pd
from datetime import date
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

tasks = pd.read_csv(DATA_DIR / "tasks.csv")
availability = pd.read_csv(DATA_DIR / "availability.csv")
from workload import calculate_workload
from prioritization import calculate_priority
from study_planner import generate_study_plan

# Load task data
tasks = pd.read_csv(DATA_DIR / "tasks.csv")

# Load available study hours
availability = pd.read_csv(DATA_DIR / "availability.csv")

print("      UNIFLOW AI STUDY PLANNER      ")

print("\nTASKS:")
print(tasks)

print("\nAVAILABLE STUDY HOURS:")
print(availability)

# Calculate workload
workload = calculate_workload(tasks)

print("\n")
print("      WORKLOAD ANALYSIS      ")
print("Total tasks:", workload["total_tasks"])
print("Total study hours required:", workload["total_hours"])
print("Average difficulty:", workload["average_difficulty"])
print("Workload level:", workload["workload_level"])


# Calculate task priorities
today = date(2026, 9, 21)

tasks["priority"] = tasks.apply(
    lambda row: calculate_priority(row, today),
    axis=1
)

# Sort tasks from highest to lowest priority
tasks = tasks.sort_values(
    by="priority",
    ascending=False
)


print("\n      TASK PRIORITY      ")

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

# Generate study plan
study_plan, remaining_hours = generate_study_plan(
    tasks,
    availability,
    today
)


print("\n      GENERATED STUDY PLAN      ")

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


# Check for unfinished tasks
unfinished_tasks = {
    task: hours
    for task, hours in remaining_hours.items()
    if hours > 0
}


if unfinished_tasks:

    print("\n===== WARNING =====")
    print("Some tasks could not be fully scheduled:")

    for task, hours in unfinished_tasks.items():
        print(f"- {task}: {hours} hour(s) remaining")

else:

    print("\nAll tasks have been scheduled successfully!")