# University Timetable Organizer and Conflict Detector

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
MAX_CLASSES_PER_DAY = 3


def get_class_count(day):
    """Ask how many classes are scheduled for a day (from 0 to 3)."""
    while True:
        try:
            count = int(input(f"How many classes do you have on {day}? "))
            if 0 <= count <= MAX_CLASSES_PER_DAY:
                return count
            print(f"Please enter a number from 0 to {MAX_CLASSES_PER_DAY}.")
        except ValueError:
            print("Please enter a whole number.")


def get_time(prompt):
    """Get a valid time in 24-hour HH:MM format and return its minutes."""
    while True:
        time_text = input(prompt).strip()

        # Check that the time has the required HH:MM shape.
        if len(time_text) == 5 and time_text[2] == ":":
            hour_text = time_text[:2]
            minute_text = time_text[3:]

            if hour_text.isdigit() and minute_text.isdigit():
                hour = int(hour_text)
                minute = int(minute_text)

                if 0 <= hour <= 23 and 0 <= minute <= 59:
                    # Convert the time to minutes after midnight.
                    return hour * 60 + minute

        print("Invalid time. Enter a time in 24-hour HH:MM format, such as 09:30.")


def minutes_to_time(total_minutes):
    """Convert minutes after midnight to a HH:MM string."""
    hour = total_minutes // 60
    minute = total_minutes % 60
    return f"{hour:02d}:{minute:02d}"


def get_class_details(class_number):
    """Ask for a course code and valid start and end times."""
    course_code = input(f"  Course code for class {class_number}: ").strip()

    while not course_code:
        print("Course code cannot be empty.")
        course_code = input(f"  Course code for class {class_number}: ").strip()

    while True:
        start_time = get_time("  Start time (HH:MM): ")
        end_time = get_time("  End time (HH:MM): ")

        if end_time > start_time:
            return {
                "course_code": course_code,
                "start": start_time,
                "end": end_time,
            }

        print("The end time must be after the start time. Please enter the times again.")


def find_conflicts(classes):
    """Return pairs of classes that overlap during the day."""
    conflicts = []

    # Compare each class with every class after it.
    for first_index in range(len(classes)):
        for second_index in range(first_index + 1, len(classes)):
            first_class = classes[first_index]
            second_class = classes[second_index]

            # These checks treat a class ending exactly when another starts
            # as not being a conflict.
            if (first_class["start"] < second_class["end"]
                    and second_class["start"] < first_class["end"]):
                conflicts.append((first_class, second_class))

    return conflicts


def display_timetable(timetable):
    """Print the timetable for each day."""
    print("\nDAILY TIMETABLE")
    print("=" * 50)

    for day in DAYS:
        print(f"\n{day}:")
        classes = timetable[day]

        if not classes:
            print("  No classes scheduled.")
        else:
            for class_info in classes:
                start = minutes_to_time(class_info["start"])
                end = minutes_to_time(class_info["end"])
                print(f"  {class_info['course_code']}: {start} - {end}")


def display_conflict_report(timetable):
    """Print conflicts for each day and the total number of conflicts."""
    print("\nCONFLICT REPORT")
    print("=" * 50)

    total_conflicts = 0

    for day in DAYS:
        conflicts = find_conflicts(timetable[day])
        total_conflicts += len(conflicts)

        if conflicts:
            print(f"\n{day}:")
            for first_class, second_class in conflicts:
                print(
                    f"  {first_class['course_code']} conflicts with "
                    f"{second_class['course_code']}."
                )

    if total_conflicts == 0:
        print("No conflicts found.")

    print(f"\nTotal number of conflicts: {total_conflicts}")


def main():
    """Collect class information, then show the timetable and report."""
    timetable = {}

    for day in DAYS:
        print(f"\nEnter classes for {day}:")
        class_count = get_class_count(day)
        timetable[day] = []

        for class_number in range(1, class_count + 1):
            print(f"\nClass {class_number}:")
            class_info = get_class_details(class_number)
            timetable[day].append(class_info)

    display_timetable(timetable)
    display_conflict_report(timetable)


# Run the program.
if __name__ == "__main__":
    main()
