import datetime


class Calendar:
    def __init__(self):
        self.events = {}

    # метод create_event
    def create_event(self, event_name, event_date, event_time, event_details):
        event_id = len(self.events) + 1
        event = {
            "id": event_id,
            "name": event_name,
            "date": event_date,
            "time": event_time,
            "details": event_details
        }
        self.events[event_id] = event
        return event_id

    # метод read_event
    def read_event(self, event_id):
        str_out = ''
        for i, ii in calendar.events[event_id].items():
            str_out = str_out + str(i) + ': ' + str(ii) + '\n'
        return str_out


calendar = Calendar()
event_name = 'event 1'
event_date = datetime.datetime.now().strftime('%Y-%m-%d')
event_time = datetime.datetime.now().time().strftime('%H:%M')
event_details = "Какое то событие"

# Создать событие с помощью метода create_event класса Calendar
event_id = calendar.create_event(event_name, event_date, event_time, event_details)

print(calendar.read_event(1))




