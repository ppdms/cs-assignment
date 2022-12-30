from calendar import monthrange
from datetime import datetime, timedelta
from years import years

def generate_calendar(mm: int, yyyy: int):
    """Given an input of month number (1 to 12) and year
    it returns a string of the calendar of the month
    including last days of last month and first days of next month
    if they so collide with the calendar

    >>> initialize()
    >>> generate_calendar(12, 2022)
    "
        ───────────────────────────────────────────────────────
           ｜ΔΕΚ 2022｜
        ───────────────────────────────────────────────────────
          ΔΕΥ｜   ΤΡΙ｜   ΤΕΤ｜   ΠΕΜ｜   ΠΑΡ｜   ΣΑΒ｜   ΚΥΡ
           28｜    29｜    30｜ [  1]｜ [  2]｜ [  3]｜ [  4]
        [  5]｜ [  6]｜ [  7]｜ [  8]｜ [  9]｜ [ 10]｜ [ 11]
        [ 12]｜ [ 13]｜ [ 14]｜ [ 15]｜ [ 16]｜ [ 17]｜ [ 18]
        [ 19]｜ [ 20]｜ [ 21]｜ [ 22]｜ [ 23]｜ [ 24]｜ [ 25]
        [ 26]｜ [ 27]｜ [ 28]｜ [ 29]｜ [ 30]｜ [ 31]｜     1
        ───────────────────────────────────────────────────────"
    """

    calendar_string = f"""
    {'─'*55}
       ｜{['ΙΑΝ', 'ΦΕΒ', 'ΜΑΡ', 'ΑΠΡ', 'ΜΑΙ', 'ΙΟΥΝ', 'ΙΟΥΛ', 'ΑΥΓ', 'ΣΕΠ', 'ΟΚΤ', 'ΝΟΕ', 'ΔΕΚ'][mm-1]} {yyyy}｜
    {'─'*55}
    {'｜ '.join(['  ΔΕΥ', '  ΤΡΙ', '  ΤΕΤ', '  ΠΕΜ', '  ΠΑΡ', '  ΣΑΒ', '  ΚΥΡ'])}
    """

    if monthrange(yyyy, mm)[0] != 0:
        last_days_of_last_month = [f"   {x}" for x in list(range(1, int(monthrange(yyyy, int(
            mm) - 1 + 12*(1 if mm == 1 else 0))[1]) + 1))[-1 * int(monthrange(yyyy, mm)[0]):]]
    else:
        last_days_of_last_month = []

    days_of_given_mm = [f'[  {day}]' if len(str(day)) == 1 else f'[ {day}]' for day in list(
        range(1, monthrange(yyyy, mm)[1] + 1))]

    first_days_of_next_month_needed_num = [f"    {x}" for x in list(range(
        1, 6 - datetime(yyyy, mm, int(days_of_given_mm[-1].replace('[ ', '').replace(']', ''))).weekday() + 1))]
    days_to_be_printed = last_days_of_last_month + \
        days_of_given_mm + first_days_of_next_month_needed_num

    eventful_days = set()
    if yyyy in years.keys():
        for event in years[yyyy][mm].events:
            eventful_days.add(event.day)

    for i in range(len(days_to_be_printed)):
        if '[' in days_to_be_printed[i]:  # CHECKS IF DATE IS FROM MONTH SELECTED
            # CHECKS IF DAY HAS AT LEAST ONE EVENT
            if int(days_to_be_printed[i].replace('[ ', '').replace(']', '')) in eventful_days:
                # CHANGES [ DAY] TO [*DAY]
                days_to_be_printed[i] = f"[*{days_to_be_printed[i].replace('[ ', '').replace(']', '')}]"

    for line in [days_to_be_printed[x:x+7] for x in range(0, len(days_to_be_printed), 7)]:
        calendar_string += '｜ '.join(line) + "\n    "
    calendar_string += '─'*55

    return calendar_string


def print_notifications():
    """Checks if events are today and after the current time and displays them"""

    now = datetime.now()

    coming_events = []
    if now.year not in years.keys():
        print("[*] Κανένα προγραμματισμένο γεγονός σήμερα")
        return
    for event in years[now.year][now.month].events:
        if event.day == now.day and event.startdate > now:  # checks if the event is today
            coming_events.append(event)
    if len(coming_events) == 0:
        print("[*] Κανένα προγραμματισμένο γεγονός σήμερα")
        return

    for event in coming_events:
        delta = event.startdate - timedelta(hours=now.hour, minutes=now.minute)
        time_str = "ώρα" if delta.hour == 1 else "ώρες"
        minute_str = "λεπτό" if delta.minute == 1 else "λεπτά"
        print(
            f"[*] Ειδοποίηση: σε {delta.hour} {time_str} και {delta.minute} {minute_str} υπάρχει προγραμματισμένο γεγονός: '{event.title}'")
