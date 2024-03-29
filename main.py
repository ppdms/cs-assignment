from src.classes import CSV, Month
from src.repl import repl
from src.calendar_utils import print_notifications
from src.years import years


def initialize(file):
    events = CSV.read(file)

    for event in events:
        if event.year not in years.keys():
            years[event.year] = {x: Month(x, event.year) for x in range(1, 13)}
        years[event.year][event.month].addEvent(event)


if __name__ == "__main__":
    initialize("events.csv")
    print('\n')
    print_notifications()
    print('\n')
    repl()
