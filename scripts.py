import random
import os
import django
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def read_file(filename):
    with open(filename, encoding='utf-8') as _file:
        return _file.readlines()


def get_random_compliment(filename='compliments.txt'):
    compliments = read_file(filename)
    compliment = random.sample(compliments, k=1)[0]
    return compliment.strip()


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
    """Only one commendation for case of combination schoolkid, lesson_date,
lesson_subject and lesson_teacher."""
    commendation_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=commendation_subject,
    ).order_by('-date').first()
    compliment = get_random_compliment()
    try:
        Commendation.objects.get(
            schoolkid=schoolkid,
            created=commendation_lesson.date,
            subject=commendation_lesson.subject,
            teacher=commendation_lesson.teacher,
        )
    except Commendation.MultipleObjectsReturned:
        pass
    except Commendation.DoesNotExist:
        Commendation.objects.create(
            schoolkid=schoolkid,
            created=commendation_lesson.date,
            subject=commendation_lesson.subject,
            teacher=commendation_lesson.teacher,
            text=compliment,
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
    child = get_child("Голубев Гремислав Антипович")

    fix_marks(schoolkid=child)
    remove_chastisements(schoolkid=child)
    create_commendation(child, 'Русский язык')


if __name__ == '__main__':
    main()

