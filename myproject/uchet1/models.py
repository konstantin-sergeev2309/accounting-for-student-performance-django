from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, User

from datetime import date

class Group(models.Model):
    name = models.CharField(max_length=5)
    master = models.ForeignKey('Prepods', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='master')
    kurator = models.ForeignKey('Prepods', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='kurator')

    def __str__(self):
        if self.master:
            return f"{self.name} - ({self.master})"
        return f"{self.name} - (Мастер не назначен)"

    def get_course(self):
        """Возвращает курс группы на основе первой цифры в названии."""
        if self.name and self.name[0].isdigit():
            return int(self.name[0])
        return 1  # По умолчанию 1 курс, если название группы не начинается с цифры

    def get_current_semester_for_group(self):
        """Возвращает текущий семестр для группы на основе текущей даты и курса."""
        today = date.today()
        course = self.get_course()

        if (today.month >= 9 and today.month <= 12):
            return (course - 1) * 2 + 1  # Первый семестр
        elif today.month >= 1 and today.month <= 6:
            return (course - 1) * 2 + 2  # Второй семестр
        else:
            return None  # Летние месяцы (июль, август) не относятся к семестрам

    def get_available_semesters(self):
        """Возвращает доступные семестры для группы (текущий и следующий/предыдущий)."""
        current_semester = self.get_current_semester_for_group()
        if current_semester is None:
            return []

        course = self.get_course()
        min_semester = (course - 1) * 2 + 1  # Минимальный семестр для курса
        max_semester = (course - 1) * 2 + 2  # Максимальный семестр для курса

        available_semesters = []
        if current_semester > min_semester:
            available_semesters.append(current_semester - 1)  # Предыдущий семестр
        available_semesters.append(current_semester)  # Текущий семестр
        if current_semester < max_semester:
            available_semesters.append(current_semester + 1)  # Следующий семестр

        return available_semesters


class Prepods(models.Model):
    name = models.CharField(max_length=50)
    predmet = models.ManyToManyField('PredM', blank=True, )
    Cab = models.ForeignKey('Cabs', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        preps = ", ".join([predmet.name for predmet in self.predmet.all()])
        return f"{self.name} - ({preps if preps else 'Предмет не назначен'})"


class PredM(models.Model): #список всех предметов
    ind = models.CharField(max_length=50, default='0')
    name = models.CharField(max_length=50)
    prepod = models.ManyToManyField('Prepods', blank=True)

    def __str__(self):
        preps = ", ".join([prepod.name for prepod in self.prepod.all()])
        return f"{self.name} {self.ind} - ({preps if preps else 'Преподаватель не назначен'})"


class Predmets(models.Model):
    name = models.ForeignKey('PredM', on_delete=models.CASCADE, related_name='pred_name')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, blank=True, null=True)
    hours_1sem = models.IntegerField(default=0)
    hours_2sem = models.IntegerField(default=0)
    hours_total = models.IntegerField(default=0)
    hours_used = models.IntegerField(default=0)
    hours_remaining = models.IntegerField(default=0)
    pairs_remaining = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.group} - {self.name}"


class Cabs(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"


@receiver(m2m_changed, sender=Prepods.predmet.through)
def sync_predm_prepods(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        if not reverse:  # Если связь изменена через Prepods
            for pk in pk_set:
                predm = PredM.objects.get(pk=pk)
                if action == 'post_add':
                    predm.prepod.add(instance)
                elif action == 'post_remove':
                    predm.prepod.remove(instance)
        else:  # Если связь изменена через PredM
            for pk in pk_set:
                prepod = Prepods.objects.get(pk=pk)
                if action == 'post_add':
                    prepod.predmet.add(instance)
                elif action == 'post_remove':
                    prepod.predmet.remove(instance)


class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Пн', 'Понедельник'),
        ('Вт', 'Вторник'),
        ('Ср', 'Среда'),
        ('Чт', 'Четверг'),
        ('Пт', 'Пятница'),
        ('Сб', 'Суббота'),
    ]

    weekday = models.CharField(max_length=2, choices=DAYS_OF_WEEK, verbose_name="День недели")
    date = models.DateField(verbose_name="Дата")
    pair_number = models.PositiveSmallIntegerField(verbose_name="Номер пары")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа")
    subject = models.ForeignKey('Predmets', on_delete=models.DO_NOTHING, verbose_name="Предмет")
    cabinet = models.ForeignKey('Cabs', on_delete=models.DO_NOTHING, verbose_name="Кабинет", blank=True, null=True)

    def __str__(self):
        return f"{self.date} ({self.weekday}) - Пара {self.pair_number}: {self.group} - {self.subject.name} в {self.cabinet}"

class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name="ФИО")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Группа", related_name='students')

    def __str__(self):
        return f"{self.name} ({self.group})"


class PA(models.Model):  # Промежуточные оценки студентов
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="Студент")
    subject = models.ForeignKey('Predmets', on_delete=models.CASCADE, verbose_name="Предмет")
    date = models.DateField(verbose_name="Дата")
    score = models.PositiveSmallIntegerField(verbose_name="Оценка", blank=True, null=True)
    semester = models.PositiveSmallIntegerField(verbose_name="Семестр", default=1)  # Добавлено поле "Семестр"

    def __str__(self):
        return f"{self.student} - {self.subject.name} ({self.date}): {self.score} (Семестр {self.semester})"


class Grade(models.Model):  # Итоговые оценки студентов
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="Студент")
    subject = models.ForeignKey('PredM', on_delete=models.CASCADE, verbose_name="Предмет")
    final_score = models.FloatField(verbose_name="Итоговая оценка", blank=True, null=True)
    semester = models.PositiveSmallIntegerField(verbose_name="Семестр", default=1)  # Добавлено поле "Семестр"

    def __str__(self):
        return f"{self.student} - {self.subject.name}: {self.final_score} (Семестр {self.semester})"


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('prepod', 'Преподаватель'),
        ('uchebnaya_chast', 'Учебная часть'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='prepod')
    prepod = models.ForeignKey('Prepods', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Преподаватель")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


