def get_day_name(number):
    if number == 1:
        return "Sunday"
    elif number == 2:
        return "Monday"
    elif number == 3:
        return "Tuesday"
    elif number == 4:
        return "Wednesday"
    else:
        return "Thursday"


def read_time(prompt):
    while True:
        value = int(input(prompt))
        hours = value // 100
        minutes = value % 100
        if value >= 0 and hours <= 23 and minutes <= 59:
            return hours * 60 + minutes
        print("Invalid time! Please use 24-hour format.")


def to_time(total):
    hours = total // 60
    minutes = total % 60
    result = ""
    if hours < 10:
        result = "0"
    result = result + str(hours) + ":"
    if minutes < 10:
        result = result + "0"
    result = result + str(minutes)
    return result


def read_class():
    code = input("Course code: ")
    while True:
        start = read_time("Start time: ")
        end = read_time("End time: ")
        if end > start:
            break
        print("End time must be after start time! Try again.")
    return code, start, end


def has_conflict(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1


conflict_count = 0

for day_number in range(1, 6):
    day = get_day_name(day_number)
    print("\n " + day + " ")

    count = int(input("Number of classes on this day (0-3): "))
    while count < 0 or count > 3:
        count = int(input("Please enter a number from 0 to 3: "))

    if count >= 1:
        code1, start1, end1 = read_class()
    if count >= 2:
        code2, start2, end2 = read_class()
    if count >= 3:
        code3, start3, end3 = read_class()

    print("\nTimetable for", day)
    if count == 0:
        print("No classes")
    if count >= 1:
        print(code1, to_time(start1), "-", to_time(end1))
    if count >= 2:
        print(code2, to_time(start2), "-", to_time(end2))
    if count >= 3:
        print(code3, to_time(start3), "-", to_time(end3))

    if count >= 2 and has_conflict(start1, end1, start2, end2):
        print("Conflict:", code1, "and", code2)
        conflict_count += 1
    if count >= 3 and has_conflict(start1, end1, start3, end3):
        print("Conflict:", code1, "and", code3)
        conflict_count += 1
    if count >= 3 and has_conflict(start2, end2, start3, end3):
        print("Conflict:", code2, "and", code3)
        conflict_count += 1

print("\n Conflict Report:")
if conflict_count == 0:
    print("No conflicts found")
else:
    print("Total conflicts:", conflict_count)
