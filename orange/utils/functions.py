import random

from member.models import Member, TeamBase


def orange_group(teambase_pk, number_of_group):
    member_list = []        # 분류할 멤버 리스트
    distributions = []      # 필터링을 거칠 랜덤 분포 목록
    survived_distribs = []  # 필터링에서 살아남은 분포 목록
    print('started')
    # 분류할 멤버 리스트 생성
    teambase = TeamBase.objects.get(pk=teambase_pk)
    members_queryset = teambase.members.all()
    for member in members_queryset:
        member_list.append(member.pk)

    # 랜덤 분포 생성
    for i in range(300):
        t = random_group(member_list, number_of_group)
        distributions.append(t)

    standard_avg_list = [
        ['age', teambase.get_standard_avg_age(), 0.3],
        ['closeness', teambase.get_standard_avg_closeness(), 0.3],
        ['activity', teambase.get_standard_avg_activity(), 0.2],
        ['leader', teambase.get_standard_avg_leader(), 0.1],
        ['clouder', teambase.get_standard_avg_clouder(), 0.1],
        ['sex', teambase.get_standard_avg_sex(), 0.2],
    ]

    # 분포 적합성 평가
    i = 0
    for standard_avg in standard_avg_list:
        i += 1
        print('process #', i)
        survived_distribs = []
        for distribution in distributions:
            # 적합성 평가
            if pass_assessment(distribution, standard_avg[0], standard_avg[1], standard_avg[2]):
                survived_distribs.append(distribution)
        print(len(survived_distribs))
        if not survived_distribs:
            pass
        # 살아남은 분포 목록을 필터링을 거칠 목록으로
        distributions = survived_distribs

    # print('생존 분포 수', len(survived_distribs))   # 생존 분포 갯수
    # print('생존 분포 리스트', survived_distribs)
    #
    # print('LIST OF MEMBER_PK')
    # for index, distribution in enumerate(survived_distribs):
    #     print(f'team #{index+1}')
    #     for team in distribution:
    #         for member_pk in team:
    #             print('member_pk', member_pk)
    #
    # avg_leader = 0
    # avg_clouder = 0
    # avg_sex = 0
    # avg_activity = 0
    # avg_age = 0
    # avg_closness = 0
    # print('LIST OF AVERAGE VALUE OF TEAM MEMBERS')
    # for index, distribution in enumerate(survived_distribs):
    #     print(f'team #{index+1}')
    #     for team in distribution:
    #         for member_pk in team:
    #             member = Member.objects.get(pk=member_pk)
    #             avg_leader += member.leader
    #             avg_clouder += member.clouder
    #             avg_sex += member.sex
    #             avg_activity += member.activity
    #             avg_age += member.age
    #             avg_closness += avg_closness
    #         avg_leader = avg_leader/len(team)
    #         avg_clouder = avg_clouder/len(team)
    #         avg_sex = avg_sex/len(team)
    #         avg_activity = avg_activity/len(team)
    #         avg_age = avg_age/len(team)
    #         avg_closness = avg_closness/len(team)
    #
    # print('avg_leader', avg_leader)
    # print('avg_clouder', avg_clouder)
    # print('avg_sex', avg_sex)
    # print('avg_activity', avg_activity)
    # print('avg_age', avg_age)
    # print('avg_closness', avg_closness)

    return survived_distribs


def random_group(member_list, number_of_group):
    # 팀을 배정할 이중 리스트 생성
    group_list = []
    for i in range(number_of_group):
        group_list.append([])
    # member_list 는 훼손하지 않으면서 랜덤 리스트 생성
    random_list = member_list
    random.shuffle(random_list)
    # n 개의 박스에 차례대로 배분. 이미 무작위 리스트이므로 결과도 무작위
    for index, member in enumerate(random_list):
        group_list[index % number_of_group].append(member)
    return group_list


def pass_assessment(distribution, factor, standard_avg, error_rate=0.5):
    """
    주어진 분포의 특정 요소 분포도가 평균치와 오차범위 내에서 일치하는가를 판단하는 함수
    쉽게 말해 잘 분배되었는가, 한 쪽으로 쏠리지는 않았는 가를 판단하는 함수

    :param distribution: team list
    :param factor: distribution factor string
    :param standard_avg: standard average. average of whole member
    :param error_rate: allowed error rate
    :return: True for pass
    """
    summation = 0
    for team in distribution:
        avg_of_team = average(team, factor)                     # 팀 평균 계산
        deviation_of_team = abs(standard_avg - avg_of_team)     # 표준편차
        summation += deviation_of_team
    avg_deviation_of_group = summation/len(distribution)        # 표준편차의 평균
    if avg_deviation_of_group <= error_rate:    # 패스 조건. 오차율보다 평균편차가 적을 때
        return True
    return False


def average(team, factor):
    """
    주어진 팀에서 특정 요소 값의 평균을 구하는 함수

    :param team: member list
    :param factor: distribution factor string
    :return: average of a certain factor in a given member list
    """
    summation = 0
    if factor == 'sex':
        for pk in team:
            summation += Member.objects.get(pk=pk).sex
    elif factor == 'leader':
        for pk in team:
            summation += Member.objects.get(pk=pk).leader
    elif factor == 'clouder':
        for pk in team:
            summation += Member.objects.get(pk=pk).clouder
    elif factor == 'age':
        for pk in team:
            summation += Member.objects.get(pk=pk).age
    elif factor == 'activity':
        for pk in team:
            summation += Member.objects.get(pk=pk).activity
    elif factor == 'closeness':
        for pk in team:
            summation += Member.objects.get(pk=pk).get_avg_of_closeness()
    return summation/len(team)
