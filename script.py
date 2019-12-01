# import csv
# import os
# import sys
# import django
# import av
# from django.db.models import Value, F, CharField, Count, Sum, OuterRef, Subquery, When, Case, IntegerField
# from django.db.models.functions import Concat
#
# os.environ["DJANGO_SETTINGS_MODULE"] = "Ballogy.settings"
# django.setup()
#
# from ballogyApi.models import Test, TestTemplate, AttemptExercise, ExerciseDetail, AthleteTest, \
#     BallogyGroup, BallogyGroupMember
#
#
# class ScriptFunctions(object):
#
#     @staticmethod
#     def create_stats_data():
#         athlete_tests = AthleteTest.objects.filter(test_status='6').exclude(athlete_id__in=[477, 476])
#         all_attempts = AttemptExercise.objects.filter(athlete_test__in=athlete_tests).values(
#             'exercise_detail__test_template__exercise__name',
#             'exercise_detail__test_template__exercise_position__position_name').annotate(
#             count=Count('exercise_detail__test_template__exercise__name'), hits=Count(Case(
#                 When(absolute_score__gt=0, then=1),
#                 output_field=IntegerField(),
#             )), miss=Count(Case(
#                 When(absolute_score=0, then=1),
#                 output_field=IntegerField(),
#             ))).order_by(
#             'exercise_detail__test_template__exercise__name',
#             'exercise_detail__test_template__exercise_position__position_name')
#         with open('shot_stats.csv', mode='w') as csv_file:
#             employee_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             employee_writer.writerow(['Shot', "Total", "Hits", "Miss", "Percentage Hits"])
#             for a in all_attempts:
#                 employee_writer.writerow(['%s/%s' % (a.get('exercise_detail__test_template__exercise__name'), a.get(
#                     'exercise_detail__test_template__exercise_position__position_name')), a.get('count'),
#                                           a.get('hits'), a.get('miss'),
#                                           str(round(100 * (a.get('hits') / float(a.get('count'))), 2))])
#
#     @staticmethod
#     def remove_duplicate_group_members():
#         all_groups = BallogyGroup.objects.all().order_by('id')
#         for group in all_groups:
#             members = BallogyGroupMember.objects.filter(group=group).order_by('member_id', 'id').distinct('member_id')
#             duplicate_members = BallogyGroupMember.objects.filter(group=group).exclude(
#                 id__in=members.values_list('id', flat=True))
#             if duplicate_members.count() > 0:
#                 print(duplicate_members)
#                 print(group.id, group.type, group.title)
#
#
#     @staticmethod
#     def generate_thumbnail():
#         container = av.open('https://ballogybucket.s3-us-west-2.amazonaws.com/dev/v/20191008072115348162/84eb7ee8-dd68-497e-ac7b-994c1714e419.mp4')
#         container.seek(container.duration//2)
#         for frame in container.decode(video=0):
#             frame.to_image().save('/home/hassan/Old/frame-%04d.jpg' % frame.index)
#             break
#
#         # for packet in container.demux():
#         #     for frame in packet.decode():
#         #         frame.to_image().save('/home/hassan/Old/frame-%04d.jpg' % frame.index)
#
#
# if __name__ == '__main__':
#     functions_list = ['generate_thumbnail']
#     for f in functions_list:
#         print('Function Name: %s' % f)
#         run_or_not = ""
#         while run_or_not not in ['y', 'n']:
#             run_or_not = input('Run (y/n)?')
#         if run_or_not == 'y':
#             getattr(ScriptFunctions, f)()
#
#     sys.exit()
