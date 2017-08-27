# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from vkApi.vkUser import VkUser
from vkApi.vkGroup import getEvent


class ServiceUser(models.Model):
    def __str__(self):
        if settings.DEBUG:
            return '%s %s' % (self.serviceUser_lastName.encode('utf8'),
                              self.serviceUser_firstName.encode('utf8'))
        else:
            return '%s %s' % (self.serviceUser_lastName.encode('utf8'),
                              self.serviceUser_firstName.encode('utf8'))

    class Meta():
        db_table = "serviceUsers"
        ordering = ['serviceUser_lastName']

    @staticmethod
    def createServiceUser(userId, accessToken):
        """Создает объект ServiceUser в базе данных

        :param userId: id пользователя
        :param accessToken: токен пользователя
        :return: None
        """
        vkUser = VkUser(userId)
        serviceUser = ServiceUser(
            serviceUser_id=userId,
            serviceUser_firstName=vkUser.getFirstName(),
            serviceUser_lastName=vkUser.getLastName(),
            serviceUser_token=accessToken,
        )
        serviceUser.save()
        for i in [1, 2, 3]:
            eventMember = EventMember(
                eventMember_owner=serviceUser,
                eventMember_event=Event.objects.get(event_id=i),
            )
            eventMember.save()

    @staticmethod
    def serviceUserExists(serviceUserId):
        return ServiceUser.objects.filter(serviceUser_id=serviceUserId).exists()

    @staticmethod
    def getServiceUser(serviceUserId):
        try:
            serviceUser = ServiceUser.objects.get(serviceUser_id=serviceUserId)
            return serviceUser
        except ServiceUser.DoesNotExist:
            # TODO добавить 400 ошибку
            raise Exception

    serviceUser_id = models.IntegerField(primary_key=True)
    serviceUser_firstName = models.CharField(max_length=100)
    serviceUser_lastName = models.CharField(max_length=100)
    serviceUser_token = models.CharField(max_length=200)
    serviceUser_image = models.URLField(blank=True, null=True)


class Event(models.Model):
    def __str__(self):
        if settings.DEBUG:
            return '%s' % (self.event_name.encode('utf8'))
        else:
            return '%s' % (self.event_name.encode('utf8'))

    class Meta():
        db_table = "events"
        ordering = ['event_id']

    @staticmethod
    def createEvent(eventId):
        vkEvent = getEvent(eventId)
        event = Event(
            event_id=eventId,
            event_name=vkEvent['name'],
            event_image=vkEvent['photo_200']
        )
        event.save()

    @staticmethod
    def eventExists(eventId):
        return Event.objects.filter(event_id=eventId).exists()

    @staticmethod
    def getEvent(eventId):
        try:
            event = Event.objects.get(event_id=eventId)
            return event
        except Event.DoesNotExist:
            pass

    @staticmethod
    def getDefaultEvents(userId):
        defaultEvents = Event.objects.filter(event_id__in=[1, 2, 3])
        events = []
        for event in defaultEvents:
            if EventMember.objects.filter(
                eventMember_event=event,
                eventMember_owner=ServiceUser.objects.get(serviceUser_id=userId)
            ).exists():
                events.append({
                    'event': event,
                    'event_status': True
                })
            else:
                events.append({
                    'event': event,
                    'event_status': False
                })

        return events

    event_id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=300)
    event_image = models.URLField(blank=True, null=True)


class EventMember(models.Model):
    class Meta():
        db_table = "eventMembers"

    @staticmethod
    def createEventMember(ownerId, eventId):
        eventMember = EventMember(
            eventMember_owner=ServiceUser.getServiceUser(ownerId),
            eventMember_event=Event.getEvent(eventId)
        )
        eventMember.save()

    @staticmethod
    def getEventMember(ownerId, eventId):
        try:
            eventMember = EventMember.objects.get(
                eventMember_owner=ServiceUser.getServiceUser(ownerId),
                eventMember_event=Event.getEvent(eventId)
            )
            return eventMember
        except EventMember.DoesNotExist:
            pass

    @staticmethod
    def eventMemberExists(ownerId, eventId):
        return EventMember.objects.filter(
            eventMember_owner=ServiceUser.getServiceUser(ownerId),
            eventMember_event=Event.getEvent(eventId),
        ).exists()

    eventMember_owner = models.ForeignKey(ServiceUser)
    eventMember_event = models.ForeignKey(Event)


class Choice(models.Model):
    @staticmethod
    def makeChoice(choice: int,
                   whoChosen: ServiceUser,
                   whomChosen: EventMember) -> None:
        """
        Создание Choice в БД.
        :param choice: оценка (1 - да, 0 - нет);
        :param whoChosen: ServiceUser, который дал оценку;
        :param whomChosen: EventMember, которому дана оценка;
        :return: None
        """
        # TODO повторное изменение Choice

        boolChoice = False
        if int(choice) == 1:
            boolChoice = True

        try:
            choice = Choice.objects.get(
                choiceList_whoChosen=whoChosen,
                choiceList_whomChosen=whomChosen,
            )
            choice.choiceList_choice = boolChoice
        except Choice.DoesNotExist:
            choice = Choice(
                choiceList_whoChosen=whoChosen,
                choiceList_whomChosen=whomChosen,
                choiceList_choice=boolChoice
            )
        choice.save()

    @staticmethod
    def getChoice(whoChosen: ServiceUser, whomChosen: EventMember):
        try:
            choice = Choice.objects.get(
                choiceList_whoChosen=whoChosen,
                choiceList_whomChosen=whomChosen
            ).choiceList_choice
            return choice
        except Choice.DoesNotExist:
            return None

    choiceList_whoChosen = models.ForeignKey(ServiceUser, related_name='whoChosen')
    choiceList_whomChosen = models.ForeignKey(EventMember, related_name='whomChosen')
    choiceList_choice = models.BooleanField()


class VisitList(models.Model):
    visitList_whoVisit = models.ForeignKey(EventMember, related_name='whoVisit')
    visitList_whomVisit = models.ForeignKey(EventMember, related_name='whomVisit')


class ShownUserList(models.Model):
    shownUserList_user = models.OneToOneField(EventMember)
    shownUserList_shownUsers = models.ManyToManyField(EventMember, related_name='shownUsers')
