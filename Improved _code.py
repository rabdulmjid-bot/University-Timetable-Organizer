# University Timetable Organizer and Conflict Detector
#
# This program asks the user for classes from Sunday to Thursday,
# organizes the timetable, and reports overlapping classes.

# A list is used to keep the days in the required order.
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

# Maximum number of classes allowed on each day.
MAX_CLASSES = 3


def get_class_count(day):
    """Ask the user for the number of classes on a day."""
    while True:
        number_text = input(f"How many classes do you have on {day}? ")

        # Try to convert the input into an integer.
        try:
            number = int(number_text)
        except ValueError:
            print("Error: Please enter a whole number.")
            continue

        # Check that the number is from 0 to 3.
        if 0 <= number <= MAX_CLASSES:
            return number
        else:
            print(f"Error: Enter a number from 0 to {MAX_CLASSES}.")


def time_to_minutes(time_text):
    """
    Convert a valid HH:MM time into minutes after midnight.

    This function returns None if the time is not in a valid format.
    """
    # A valid 24-hour time must contain exactly five characters.
    if len(time_text) != 5:
        return None

    # The third character must be a colon.
    if time_text[2] != ":":
        return None

    hour_text = time_text[:2]
    minute_text = time_text[3:]

    # Both parts of the time must contain only digits.
    if not hour_text.isdigit() or not minute_text.isdigit():
        return None

    hour = int(hour_text)
    minute = int(minute_text)

    # HH can be from 00 to 23 and MM can be from 00 to 59.
    if hour < 0 or hour > 23:
        return None

    if minute < 0 or minute > 59:
        return None

    # Convert hours and minutes into total minutes.
    total_minutes = (hour * 60) + minute
    return total_minutes


def get_valid_time(prompt):
    """Repeatedly ask until the user enters a valid HH:MM time."""
    while True:
        user_input = input(prompt).strip()
        minutes = time_to_minutes(user_input)

        if minutes is not None:
            return minutes

        print("Error: Enter a valid 24-hour time in HH:MM format.")
        print("Example: 09:30 or 14:45")


def minutes_to_time(total_minutes):
    """Convert minutes after midnight into an HH:MM string."""
    hour = total_minutes // 60
    minute = total_minutes % 60
    return f"{hour:02d}:{minute:02d}"


def get_course_code(class_number):
    """Ask the user for a course code and prevent an empty answer."""
    while True:
        course_code = input(
            f"  Enter course code for class {class_number}: "
        ).strip()

        if course_code != "":
            return course_code

        print("Error: Course code cannot be empty.")


def get_class_details(class_number):
    """
    Ask for one class and return it as a dictionary.

    The dictionary stores the course code, start time, and end time.
    """
    course_code = get_course_code(class_number)

    # Keep asking until the end time is later than the start time.
    while True:
        start_time = get_valid_time("  Enter start time (HH:MM): ")
        end_time = get_valid_time("  Enter end time (HH:MM): ")

        if end_time > start_time:
            break

        print("Error: End time must be after start time.")
        print("Please enter the start and end times again.")

    # Return all the information for this one class.
    return {
        "course_code": course_code,
        "start": start_time,
        "end": end_time
    }


def enter_timetable():
    """Enter and organize the timetable for all five days."""
    timetable = {}

    # Repeat once for each day in the DAYS list.
    for day in DAYS:
        print(f"\n--- Enter classes for {day} ---")

        # Ask for the number of classes on this particular day.
        class_count = get_class_count(day)

        # Create an empty list for this day.
        timetable[day] = []

        # Use range to add the correct number of classes.
        for class_number in range(1, class_count + 1):
            class_details = get_class_details(class_number)
            timetable[day].append(class_details)

    return timetable


def find_conflicts(classes):
    """
    Find overlapping classes in a list for the same day.

    Each conflict is stored as two class dictionaries.
    """
    conflicts = []

    # Compare every class with every later class in the list.
    for first_index in range(len(classes)):
        first_class = classes[first_index]

        for second_index in range(first_index + 1, len(classes)):
            second_class = classes[second_index]

            # Two classes conflict when their time ranges overlap.
            # Classes that meet exactly at a boundary do not conflict.
            overlap = (
                first_class["start"] < second_class["end"]
                and
                second_class["start"] < first_class["end"]
            )

            if overlap:
                conflicts.append((first_class, second_class))

    return conflicts


def display_timetable(timetable):
    """Display the timetable using HH:MM time format."""
    print("\nDAILY TIMETABLE")
    print("=" * 50)

    for day in DAYS:
        print(f"\n{day}:")

        # Get the list of classes for this day.
        classes = timetable[day]

        if len(classes) == 0:
            print("  No classes scheduled.")
        else:
            # Print every class stored for this day.
            for class_details in classes:
                start_text = minutes_to_time(class_details["start"])
                end_text = minutes_to_time(class_details["end"])

                print(
                    f"  {class_details['course_code']}: "
                    f"{start_text} - {end_text}"
                )


def display_conflict_report(timetable):
    """Display conflicts and the total number of conflicts."""
    print("\nFINAL CONFLICT REPORT")
    print("=" * 50)

    total_conflicts = 0

    # Check conflicts separately for every day.
    for day in DAYS:
        classes = timetable[day]
        conflicts = find_conflicts(classes)

        # Add this day's conflicts to the overall total.
        total_conflicts = total_conflicts + len(conflicts)

        # Print this day's conflicts, if there are any.
        if len(conflicts) > 0:
            print(f"\n{day}:")

            for first_class, second_class in conflicts:
                print(
                    f"  Conflict: {first_class['course_code']} overlaps "
                    f"with {second_class['course_code']}."
                )

    # If no conflicts were found on any day, print a simple message.
    if total_conflicts == 0:
        print("\nNo conflicts found.")
    else:
        print("")  # Add a blank line before the final summary.

    print(f"Total number of conflicts: {total_conflicts}")


def main():
    """Organize the complete timetable program."""
    print("UNIVERSITY TIMETABLE ORGANIZER")
    print("=" * 50)

    timetable = enter_timetable()
    display_timetable(timetable)
    display_conflict_report(timetable)


# Start the program only when this file is run directly.
if __name__ == "__main__":
    main()
