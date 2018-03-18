from django.db import models


class Member(models.Model):
    LEADER_CHOICE = ((1, 'leader'), (0, 'not_leader'))
    CLOUDER_CHOICE = ((1, 'clouder'), (0, 'not_clouder'))
    SEX_CHOICE = ((1, 'male'), (0, 'female'))

    name = models.CharField(max_length=5, blank=False)
    team = models.ForeignKey(
        'Team', related_name='members', on_delete=models.CASCADE)
    base = models.ForeignKey(
        'TeamBase', related_name='members', on_delete=models.CASCADE)

    leader = models.IntegerField(choices=LEADER_CHOICE)
    clouder = models.IntegerField(choices=CLOUDER_CHOICE)
    sex = models.IntegerField(choices=SEX_CHOICE)
    activity = models.IntegerField()
    age = models.IntegerField()
    closeness = models.ManyToManyField(
        'Member', symmetrical=False, through='Closeness', null=True,
        verbose_name='closeness_with', related_name='closeness_with')

    def get_avg_of_closeness(self):
        if not len(self.closeness_to.all()):
            return 0
        summation = 0
        for rel in self.closeness_to.all():
            summation += rel.closeness
        return summation/len(self.closeness.all())


class Team(models.Model):
    name = models.CharField(max_length=32, blank=False)
    base = models.ForeignKey(
        'TeamBase', related_name='teams', on_delete=models.CASCADE)


class TeamBase(models.Model):
    name = models.CharField(max_length=32, blank=False)

    def get_standard_avg_leader(self):
        if not len(self.members.all()):
            return 0
        summation = 0
        for member in self.members.all():
            summation += member.leader
        return summation/len(self.members.all())

    def get_standard_avg_clouder(self):
        if not len(self.members.all()):
            return 0
        summation = 0
        for member in self.members.all():
            summation += member.clouder
        return summation/len(self.members.all())

    def get_standard_avg_sex(self):
        if not len(self.members.all()):
            return 0
        summation = 0
        for member in self.members.all():
            summation += member.sex
        return summation/len(self.members.all())

    def get_standard_avg_activity(self):
        if not len(self.members.all()):
            return 0
        summation = 0
        for member in self.members.all():
            summation += member.activity
        return summation/len(self.members.all())

    def get_standard_avg_age(self):
        if not len(self.members.all()):
            return 0
        summation = 0
        for member in self.members.all():
            summation += member.age
        return summation/len(self.members.all())

    def get_standard_avg_closeness(self):
        if not len(self.members.all()):
            return 0
        summation = 0
        for member in self.members.all():
            summation += member.get_avg_of_closeness()
        return summation/len(self.members.all())


class Closeness(models.Model):
    friend_from = models.ForeignKey(
        'Member', on_delete=models.CASCADE,
        related_name='closeness_to'
    )
    friend_to = models.ForeignKey(
        'Member', on_delete=models.CASCADE,
        related_name='closeness_from'
    )
    closeness = models.IntegerField()

    def __str__(self):
        return f'"{self.closeness}: closeness between ' \
               f'{self.friend_from.name}" and "{self.friend_to.name}"'




