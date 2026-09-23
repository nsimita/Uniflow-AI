import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
csv_file = BASE_DIR / "uniflow_course_data.csv"


def prerequisite_satisfied(prerequisite, completed_courses):

    if pd.isna(prerequisite) or str(prerequisite).strip() in ["", "X"]:
        return True

    prerequisite = str(prerequisite).strip()

    prerequisites = [
        p.strip()
        for p in prerequisite.split(",")
    ]

    return all(
        p in completed_courses
        for p in prerequisites
    )


def recommend_courses(
    completed_courses,
    current_courses,
    maximum_courses,
    maximum_credits,
    preferred_courses
):

    courses = pd.read_csv(csv_file)

    taken_courses = (
        completed_courses +
        current_courses
    )

    # Remove completed and current courses
    available_courses = courses[
        ~courses["course_code"].isin(taken_courses)
    ].copy()

    # Check prerequisites
    available_courses["prerequisite_ok"] = (
        available_courses["prerequisite"].apply(
            lambda x: prerequisite_satisfied(
                x,
                completed_courses
            )
        )
    )

    available_courses = available_courses[
        available_courses["prerequisite_ok"]
    ].copy()

    # Maximum credit filter
    eligible_courses = available_courses[
        available_courses["credit"] <= maximum_credits
    ].copy()

    # Mark preferred courses
    eligible_courses["preferred"] = (
        eligible_courses["course_code"].isin(
            preferred_courses
        )
    )

    # Sort preferred courses first
    eligible_courses = eligible_courses.sort_values(
        by="preferred",
        ascending=False
    )

    # Maximum number of courses
    recommended = eligible_courses.head(
        maximum_courses
    )

    return recommended



# TEST / DEMO

def run_test():
    print("\n" + "=" * 60)
    print("             UniFlow AI - Course Recommendation")
    print("=" * 60)

    # Student information
    completed_courses = [
        "CSE 1110",
        "MATH 1151"
    ]

    current_courses = [
        "ENG 1011",
        "PHY 2106",
        "CSE 2213"
    ]

    maximum_courses = 6
    maximum_credits = 10

    preferred_courses = [
        "CSE 2213",
        "CSE 2215",
        "MATH 2183",
        "PHY 2105"
    ]

    print("\nStudent Information")
    print("-" * 60)

    print("Completed courses:")
    for course in completed_courses:
        print(f"  - {course}")

    print("\nCurrent courses:")
    for course in current_courses:
        print(f"  - {course}")

    print(f"\nMaximum number of courses: {maximum_courses}")
    print(f"Maximum credits: {maximum_credits}")

    print("\nPreferred courses:")
    for course in preferred_courses:
        print(f"  - {course}")

    # Generate recommendations
    recommended = recommend_courses(
        completed_courses,
        current_courses,
        maximum_courses,
        maximum_credits,
        preferred_courses
    )

    # Display recommendations
    print("\n" + "=" * 60)
    print("              RECOMMENDED COURSES")
    print("=" * 60)

    if recommended.empty:
        print("No courses found matching the requirements.")

    else:
        for _, course in recommended.iterrows():
            print(
                f"\nCourse Code : {course['course_code']}"
                f"\nCourse Name : {course['course_name']}"
                f"\nCredit      : {course['credit']}"
                f"\nPrerequisite: {course['prerequisite']}"
            )
            print("-" * 60)


if __name__ == "__main__":
    run_test()