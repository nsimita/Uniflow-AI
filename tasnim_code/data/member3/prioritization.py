from datetime import datetime


def calculate_priority(row, today):
    deadline = datetime.strptime(row["deadline"], "%Y-%m-%d").date()

    days_left = (deadline - today).days

    # Calculate urgency based on deadline
    if days_left <= 1:
        urgency = 5
    elif days_left <= 3:
        urgency = 4
    elif days_left <= 5:
        urgency = 3
    elif days_left <= 7:
        urgency = 2
    else:
        urgency = 1

    # Calculate final priority
    priority = (
        (urgency * 2)
        + row["difficulty"]
        + row["required_hours"]
    )

    return priority