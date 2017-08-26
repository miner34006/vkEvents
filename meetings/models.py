# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from vkApi.vkUser import VkUser
from vkApi.vkGroup import getEvent


class EventMember(models.Model):
    def __str__(self):
        if settings.DEBUG:
            return '%s %s' % (self.eventMember_lastName.encode('utf8'),
                              self.eventMember_firstName.encode('utf8'))
        else:
            return '%s %s' % (self.eventMember_lastName.encode('utf8'),
                              self.eventMember_firstName.encode('utf8'))

    class Meta():
        db_table = "eventMembers"
        ordering = ['eventMember_lastName']

    @staticmethod
    def getEventMember(id):
        """Получение объекта EventMember с eventMember_id = id
        
        :param id: id пользователя
        :return: объект EventMember
        """
        return EventMember.objects.get(eventMember_id=id)

    @staticmethod
    def getToken(id):
        """Получение eventMember_token с eventMember_id = id
        
        :param id: id пользователя
        :return: токен пользователя
        """
        return EventMember.getEventMember(id).eventMember_token


    @staticmethod
    def eventMemberExist(userId):
        return EventMember.objects.filter(eventMember_id=userId).exists()

    @staticmethod
    def createEventMember(userId, accessToken):
        """Создает объект EventMember в базе данных
        
        :param userId: id пользователя
        :param accessToken: токен пользователя
        :return: None
        """
        vkUser = VkUser(userId)
        eventMember = EventMember(
            eventMember_id=userId,
            eventMember_firstName=vkUser.getFirstName(),
            eventMember_lastName=vkUser.getLastName(),
            eventMember_token=accessToken,
        )
        eventMember.save()
        serviceEvents = Event.objects.filter(event_id__in=[1, 2, 3])
        for event in serviceEvents:
            event.event_members.add(eventMember)


    eventMember_id = models.IntegerField(primary_key=True)
    eventMember_firstName = models.CharField(max_length=100)
    eventMember_lastName = models.CharField(max_length=100)
    eventMember_token = models.CharField(max_length=200)
    eventMember_image = models.URLField(blank=True, null=True)

    #eventMember_visited = models.


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
        event = Event(
            event_id=eventId,
            event_name=getEvent(eventId)['name'],
            event_image=getEvent(eventId)['photo_200']
        )
        event.save()

    @staticmethod
    def eventExist(eventId):
        return Event.objects.filter(event_id=eventId).exists()

    @staticmethod
    def getEvent(eventId):
        return Event.objects.get(event_id=eventId)

    @staticmethod
    def getDefaultEvents(userId):
        defaultEvents = Event.objects.filter(event_id__in=[1, 2, 3])
        events = []
        for event in defaultEvents:
            if event.event_members.filter(eventMember_id=userId).exists():
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


    @staticmethod
    def getEventMembers(eventId, userId):
        return Event.getEvent(eventId=eventId).event_members.exclude(eventMember_id=userId)

    event_id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=300)
    event_image = models.URLField(blank=True, null=True)
    event_members = models.ManyToManyField(EventMember)


class ShownUserList(models.Model):
    shownUserList_user = models.OneToOneField(EventMember)
    shownUserList_shownUsers = models.ManyToManyField(EventMember, related_name='shownUsers')


class ChoiceList(models.Model):
    @staticmethod
    def makeChoice(choice, whoChoosen, whomChoosen, event):
    #todo event fix

        boolChoice = False
        if choice == 1:
            boolChoice = True

        try:
            choice = ChoiceList.objects.get(
                choiceList_whoChoosen=whoChoosen,
                choiceList_whomChoosen=whomChoosen,
                choiceList_event=whomChoosen.event_set.last(),
            )
            choice.choiceList_choice = boolChoice

        except ChoiceList.DoesNotExist:
            choice = ChoiceList(
                choiceList_whoChoosen=whoChoosen,
                choiceList_whomChoosen=whomChoosen,
                choiceList_event=whomChoosen.event_set.last(),
                choiceList_choice=boolChoice
            )
        choice.save()

    choiceList_whoChoosen = models.ForeignKey(EventMember, related_name='whoChoosen')
    choiceList_whomChoosen = models.ForeignKey(EventMember, related_name='whomChoosen')
    choiceList_event = models.ForeignKey(Event)
    choiceList_choice = models.BooleanField()


class VisitList(models.Model):
    visitList_whoVisit = models.ForeignKey(EventMember, related_name='whoVisit')
    visitList_whomVisit = models.ForeignKey(EventMember, related_name='whomVisit')
