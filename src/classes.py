from itertools import chain
from re import fullmatch
from datetime import datetime, timedelta
from functools import reduce
from src.years import years


class CSV:
    def read(filename):
        """Reads a csv file and return an array of event objects. 
        If the file doesnt exist, it creates it
        """
        while True:
            try:
                with open(filename, 'r', encoding="utf-8") as file:
                    return list(map(lambda x: Event(list(map(lambda x: int(x), x[0].split('-'))) + list(map(lambda x: int(x), x[1].split(':'))) + [int(x[2])] + [x[3]]), list(map(lambda x: [fullmatch(r"^([^,]+),([^,]+),([^,]+),([^,]+)$", x).group(i) for i in range(1, 5)], file.read().splitlines()[1:]))))

            except FileNotFoundError:
                with open(filename, 'w', encoding="utf-8") as file:
                    file.write("")
                continue

    def write(filename):
        """Given a csv file it stores the years dictionary in the csv file
        """
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("\n".join(["Date,Hour,Duration,Title"] + list(map(lambda x: f"{x.year}-{x.month}-{x.day},{x.hour}:{x.minutes:02d},{x.duration},{x.title}",
                                                                         chain.from_iterable([years[i][j].events for i in years.keys() for j in years[i]])))))


class Event:
    def __init__(self, ls):
        self.year, self.month, self.day, self.hour, self.minutes, self.duration, self.title = ls
        self.startdate = datetime(
            self.year, self.month, self.day, self.hour, self.minutes)
        self.enddate = self.startdate+timedelta(minutes=self.duration)

    def checkOverlap(self):
        """Checks if the event is overlaping with any other event,
        If it is, it prints a table with the occupied hours of the day of the event.
        """

        events = []
        # For each previous year from the events year
        for year in filter(lambda x: x < self.year, years.keys()):
            # Adding to events the events that end after this event starts
            events.extend(reduce(
                lambda x, y: x+y, [years[year][month].events for month in range(1, 13)]))
        # For each event in this events year, up to the next month this events month ->
        # Adding to the events the events that end after this event starts
        events.extend(reduce(
            lambda x, y: x+y, [years[self.year][month].events for month in range(1, self.month+1)]))

        flag = False

        for event in filter(lambda x: x.enddate >= self.startdate, events):
            if (event.enddate > self.startdate and event.startdate < self.enddate):  # Checks for collision
                flag = True
                # Creates day dictionary
                day = {x: {x: False for x in range(60)} for x in range(24)}
                # Loops over the day of the event with one minute steps
                i = datetime(event.year, event.month, event.day)

                while i < datetime(event.year, event.month, event.day) + timedelta(days=1):
                    # Checks for this minute if any event is taking place
                    day[i.hour][i.minute] = any(event.startdate <= i <=
                                                event.enddate for event in events)
                    i += timedelta(minutes=1)

                # Creates overlap table
                freecells = "  hours horizontally, minutes vertically, allocated minutes are \"++\":\n   00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23\n"
                for x in range(60):
                    freecells += f"{x:02d} " + "".join(f"{plus} " for plus in [
                        "++" if day[hour][x] else "  " for hour in range(24)])+"\n"

        return [flag, freecells if flag else None]


class Month:
    def __init__(self, mm: int, yyyy: int):
        self.month = mm
        self.year = yyyy
        self.events = []

    def addEvent(self, newevent):
        if newevent.year == self.year and newevent.month == self.month:
            self.events.append(newevent)
            return True
        else:
            return False

    def removeEvent(self, event):
        if event in self.events:
            self.events.remove(event)
            return True
        else:
            return False

    def printEvents(self):
        if len(self.events) > 0:
            for index, event in enumerate(self.events):
                print(
                    f"{index}. [{event.title}] -> Date: {event.year}-{event.month}-{event.day}, Time: {event.hour}:{event.minutes:02d}, Duration: {event.duration}")
            print()
            return self.events
        else:
            print("[-] Κανένα γεγονός αυτόν τον μήνα")
            return []
