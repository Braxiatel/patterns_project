"""
    Module for sending email/sms notifications to subscribers on updates.
"""


class Observer:

    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for observer in self.observers:
            observer.update(self)

    def notify_location(self):
        for observer in self.observers:
            observer.location_update(self)

    def notify_date(self):
        for observer in self.observers:
            observer.date_update(self)


class EmailNotify(Observer):
    def update(self, subject):
        print('[EMAIL] ->', 'joined us', subject.students[-1].name)

    @staticmethod
    def location_update(subject):
        print('[EMAIL] ->', 'location changed to', subject.location)

    @staticmethod
    def date_update(subject):
        print('[EMAIL] ->', 'start date changed to', subject.start_date)


class SMSNotify(Observer):
    def update(self, subject):
        print('[SMS] ->', 'joined us', subject.students[-1].name)

    @staticmethod
    def location_update(subject):
        print('[SMS] ->', 'location changed', subject.location)

    @staticmethod
    def date_update(subject):
        print('[SMS] ->', 'start date changed to', subject.start_date)



