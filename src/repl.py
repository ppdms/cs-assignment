from datetime import datetime
from re import fullmatch
from src.calendar_utils import generate_calendar
from calendar import monthrange
from src.classes import Event, Month, CSV
from src.years import years


def getEventInfo():
    while True:  # Get event date (registration)
        answer = input("[+] Ημερομηνία γεγονότος (yyyy-mm-dd): ")
        if fullmatch(r"\d\d\d\d\-\d\d?\-\d\d?", answer) == None:
            continue
        year, month, day = map(lambda x: int(x), answer.split("-"))
        if not 0 < month <= 12:
            continue
        months_days = monthrange(year, month)[1]
        if 0 < day <= months_days:
            break

    while True:  # Get event time (registrtation)
        answer = input("[+] Ωρα γεγονότος (hh:mm): ")
        if fullmatch(r"\d\d?\:\d\d", answer) == None:
            continue
        hour, minutes = map(
            lambda x: int(x), answer.split(":"))
        if 0 <= hour <= 23 and 0 <= minutes < 60:
            break

    while True:  # Get event duration (registration)
        answer = input("[+] Διάρκεια γεγονότος: ")
        if answer.isdigit() and int(answer) > 0:
            duration = int(answer)
            break

    while True:  # Get event name (registration)
        answer = input("[+] Τίτλος γεγονότος: ")
        if "," not in answer and len(answer) > 0:
            title = answer
            break

    if year not in years.keys():
        years[year] = {x: Month(x, year) for x in range(1, 13)}

    return [year, month, day, hour, minutes, duration, title]


def updateEventInfo(event, onlyTime=False):
    while True:  # Get event's new date
        answer = input(
            f"[+] Ημερομηνία γεγονότος ({event.year}-{event.month}-{event.day}): ") or f"{event.year}-{event.month}-{event.day}"
        if fullmatch(r"\d\d\d\d\-\d\d?\-\d\d?", answer) == None:
            continue
        year, month, day = map(lambda x: int(x), answer.split("-"))
        if not 0 < month <= 12:
            continue
        months_days = monthrange(year, month)[1]
        if 0 < day <= months_days:
            break

    while True:  # Get event's new time
        answer = input(
            f"[+] Ώρα γεγονότος ({event.hour}:{event.minutes:02d}): ") or f"{event.hour}:{event.minutes:02d}"
        if fullmatch(r"\d\d?\:\d\d", answer) == None:
            continue
        hour, minutes = map(lambda x: int(x), answer.split(":"))
        if 0 <= hour <= 23 and 0 <= minutes < 60:
            break

    if onlyTime:
        duration, title = event.duration, event.title
    else:
        while True:  # Get event's new duration
            answer = input(
                f"[+] Διάρκεια γεγονότος ({event.duration}): ") or f"{event.duration}"
            if answer.isdigit() and int(answer) > 0:
                duration = int(answer)
                break

        while True:  # Get event's new name
            answer = input(
                f"[+] Τίτλος γεγονότος ({event.title}): ") or f"{event.title}"
            if "," not in answer and len(answer) > 0:
                title = answer
                break

    if year not in years.keys():
        years[year] = {x: Month(x, year) for x in range(1, 13)}

    return [year, month, day, hour, minutes, duration, title]


def eventSearch():
    while True:  # Get event year
        answer = input("[+] Εισάγετε έτος: ")
        if answer.isdigit():
            year = int(answer)
            break

    while True:  # Get event month
        answer = input("[+] Εισάγετε μήνα: ")
        if not answer.isdigit():
            continue
        month = int(answer)
        if 0 < month <= 12:
            break

    print(f"\n{'='*37} Αναζήτηση γεγονότων {'='*37}\n")

    # Check if selected mm/yyyy has events. If events exist print them
    if year not in years.keys():
        years[year] = {x: Month(x, year) for x in range(1, 13)}
    events = years[year][month].printEvents()
    return events, len(events)


def repl():
    mm, yyyy = datetime.now().month, datetime.now().year

    while True:
        print(f"\n{'='*80}\n{generate_calendar(mm, yyyy)}")

        choice = input('''
Πατήστε ENTER για προβολή του επόμενου μήνα, "q" για έξοδο ή κάποια από τις παρακάτω επιλογές:
    "-" για πλοήγηση στον προηγούμενο μήνα
    "+" για διαχείριση των γεγονότων του ημερολογίου
    "*" για εμφάνιση των γεγονότων ενός επιλεγμένου μήνα
    -> ''')

        match choice:  # requires Py3.10
            # First menu [calendar and choice for function(navigate months, edit events, print events)]
            case "":    # User enters ENTER
                mm, yyyy = mm % 12 + 1, yyyy + 1*(mm == 12)
            case "-":   # User enters "-"
                mm, yyyy = mm - 1 + 12*(mm == 1), yyyy - 1*(mm == 1)
            case "+":   # User enters "+"
                while True:  # Always expect user input
                    choice = input('''
Διαχείριση γεγονότων ημερολογίου, επιλέξτε ενέργεια:
    1 Καταγραφή νέου γεγονότος
    2 Διαγραφή γεγονότος
    3 Ενημέρωση γεγονότος
    0 Επιστροφή στο κυρίως μενού
    -> ''')
                    match choice:
                        case "0":   # If user enters 0 go to main menu
                            break

                        case "1":   # If user enters 1 get input for event registration
                            event = Event(getEventInfo())
                            # Check if event (to be registered) is overlapping with another event
                            overlap = event.checkOverlap()
                            # If overlapping: loop until event is not overlapping
                            while overlap[0]:
                                print(
                                    "[+] Γεγονός έχει επικάλυψη με άλλα γεγονότα\n", overlap[1])
                                event = Event(updateEventInfo(
                                    event, onlyTime=True))
                                overlap = event.checkOverlap()
                            # Register event
                            years[event.year][event.month].addEvent(event)
                            print(
                                f"[+] Το γεγονός προστέθηκε: <[{event.title}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}:{event.minutes:02d}, Duration: {event.duration}>")
                            break

                        case "2":   # If user enters 2 get input for event deletion
                            events, events_len = eventSearch()
                            if events_len == 0:
                                continue

                            # If events exist in selected mm/yyyy select event (for deletion)
                            while True:
                                answer = input(
                                    "[+] Επιλέξτε γεγονός προς διαγραφή: ")
                                if not answer.isdigit():
                                    continue
                                event = int(answer)
                                if 0 <= event < events_len:
                                    break
                            event = events[event]
                            # Delete selected event
                            years[event.year][event.month].removeEvent(event)
                            print(
                                f"[+] Το γεγονός διαγράφηκε: <[{event.title}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}:{event.minutes:02d}, Duration: {event.duration}>")
                            break

                        case "3":   # If user enters 3 get input for event update
                            # Print events registered in that mm/yyyy (if any)
                            events, events_len = eventSearch()
                            if events_len == 0:
                                continue

                            # If events exist in selected mm/yyyy select event (for update)
                            while True:
                                answer = input(
                                    "[+] Επιλέξτε γεγονός προς ενημέρωση: ")
                                if not answer.isdigit():
                                    continue
                                event = int(answer)
                                if 0 <= event < events_len:
                                    break
                            event = events[event]
                            new_event = Event(updateEventInfo(event))
                            # Remove event temporarily so there are no overhead overlaps
                            years[event.year][event.month].removeEvent(event)

                            # Check if event (to be registered) is overlapping with another event
                            overlap = new_event.checkOverlap()

                            # If overlapping: loop until event is not overlapping
                            while overlap[0]:
                                print(
                                    "[-] Γεγονός έχει επικάλυψη με άλλα γεγονότα\n", overlap[1])

                                new_event = Event(updateEventInfo(
                                    new_event, onlyTime=True))
                                overlap = new_event.checkOverlap()

                            # Register edited event
                            years[new_event.year][new_event.month].addEvent(
                                new_event)
                            print(
                                f"[*] Το γεγονός ενημερώθηκε: <[{new_event.title}] -> Date: {new_event.year}-{new_event.month}-{new_event.day}, Time: {new_event.hour}:{new_event.minutes:02d}, Duration: {new_event.duration}>")
                            break

            case "*":   # If user enters "*" Then print events of entered month
                eventSearch()
                input(
                    "[+] Πατήστε οποιοδήποτε χαρακτήρα για επιστροφή στο κυρίως μενού: ")

            case "q":
                CSV.write("events.csv")
                raise SystemExit(0)
