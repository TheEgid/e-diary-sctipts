import random
import os
import django
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def read_file(filename):
    with open(filename, encoding='utf-8') as _file:
        return _file.readlines()


def get_random_compliment(filename='compliments.txt'):
    compliments = read_file(filename)
    compliments_list = [compliment.strip() for compliment in compliments]
    return random.sample(compliments_list, k=1)[0]


def fix_marks(schoolkid, bad_mark_limit=3, good_mark=5):
    bad_marks_records = Mark.objects.filter(
        schoolkid=schoolkid,
        points__lte=bad_mark_limit,
    )
    for record in bad_marks_records:
        record.points = good_mark
        record.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(
        schoolkid=schoolkid
    )
    chastisements.delete()


def get_child(_child_name):
    try:
        child = Schoolkid.objects.get(full_name__contains=_child_name)
        return child
    except ObjectDoesNotExist:
        print(f"No this entry in database: {_child_name}")
        raise SystemExit
    except MultipleObjectsReturned:
        children = Schoolkid.objects.filter(full_name__contains=_child_name)
        print("More than one entry in the database: ")
        [print(child) for child in children]
        raise SystemExit


def create_commendation(schoolkid, commendation_subject):
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=commendation_subject,
    ).order_by('-date')
    commendation_lesson = lessons[0]
    compliment = get_random_compliment()
    if not Commendation.objects.filter(
            schoolkid=schoolkid,
            subject=commendation_lesson.subject,
            teacher=commendation_lesson.teacher,
            created=commendation_lesson.date,
    ):
        Commendation.objects.create(
            schoolkid=schoolkid,
            text=compliment,
            created=commendation_lesson.date,
            subject=commendation_lesson.subject,
            teacher=commendation_lesson.teacher,
        )


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
    from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
    global Schoolkid
    global Mark
    global Chastisement
    global Lesson
    global Commendation
    
    #  customizations
    child = get_child("Хохлова Ульяна Афанасьевна")
    
    fix_marks(schoolkid=child)
    remove_chastisements(schoolkid=child)
    create_commendation(child, 'Русский язык')

    
if __name__ == '__main__':
    main()

