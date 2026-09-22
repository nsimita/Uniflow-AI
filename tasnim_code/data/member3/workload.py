def calculate_workload(tasks):
    total_tasks = len(tasks)
    total_hours = tasks["required_hours"].sum()
    average_difficulty = tasks["difficulty"].mean()

    if total_hours >= 12:
        workload_level = "High"
    elif total_hours >= 6:
        workload_level = "Medium"
    else:
        workload_level = "Low"

    return {
        "total_tasks": total_tasks,
        "total_hours": total_hours,
        "average_difficulty": round(average_difficulty, 2),
        "workload_level": workload_level
    }