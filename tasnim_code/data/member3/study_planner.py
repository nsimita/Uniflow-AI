import pandas as pd
from datetime import datetime, timedelta


def generate_study_plan(tasks, availability, start_date):
    plan = []

    # Make a copy so we don't change the original data
    tasks = tasks.copy()

    # Convert deadlines into dates
    tasks["deadline"] = pd.to_datetime(tasks["deadline"]).dt.date

    # Track remaining study hours for each task
    remaining_hours = {}

    for _, task in tasks.iterrows():
        remaining_hours[task["task_name"]] = task["required_hours"]

    # Process each available study day
    for day_number, (_, day_info) in enumerate(availability.iterrows()):

        day_name = day_info["day"]
        available_hours = day_info["available_hours"]

        current_date = start_date + timedelta(days=day_number)

        # Only consider tasks whose deadline has not passed
        available_tasks = tasks[
            tasks["deadline"] >= current_date
        ]

        # Sort by priority
        available_tasks = available_tasks.sort_values(
            by="priority",
            ascending=False
        )

        # Allocate study hours
        for _, task in available_tasks.iterrows():

            task_name = task["task_name"]

            if remaining_hours[task_name] <= 0:
                continue

            hours = min(
                remaining_hours[task_name],
                available_hours
            )

            if hours > 0:

                plan.append({
                    "day": day_name,
                    "date": current_date,
                    "task": task_name,
                    "course": task["course"],
                    "hours": hours
                })

                remaining_hours[task_name] -= hours
                available_hours -= hours

            if available_hours <= 0:
                break

    return plan, remaining_hours