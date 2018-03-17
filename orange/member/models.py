from django.db import models


class Member(models.Model):
    LEADER_CHOICE = ((1, 'leader'), (0, 'not_leader'))
    CLOUDER_CHOICE = ((1, 'clouder'), (0, 'not_clouder'))
    SEX_CHOICE = ((1, 'male'), (0, 'female'))

    name = models.CharField(max_length=5, blank=False)
    leader = models.IntegerField(choices=LEADER_CHOICE)
    clouder = models.IntegerField(choices=CLOUDER_CHOICE)
    sex = models.IntegerField(choices=SEX_CHOICE)
    activity = models.IntegerField()
    age = models.IntegerField()
    closeness = models.ManyToManyField(
        'Member', symmetrical=False, through='Closeness',
        )


class Closeness(models.Model):
    pass



