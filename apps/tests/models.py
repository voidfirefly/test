import uuid

from django.utils import timezone
from django.core.cache import cache

from django.db import models
from django.contrib.auth.models import User

from courses.models import Course

from .utils import TestControllerRandom


class Test(models.Model):

    ESTIMATE_METHODS = (
        ('default', 'Стандартный'),
        ('many_answers', 'Множество ответов'),
    )

    course = models.ManyToManyField(Course)
    title = models.CharField('Название', max_length=255)
    slug = models.SlugField('Slug')
    description = models.TextField('Описание')
    estimate_method = models.CharField(
        'Метод оценки', choices=ESTIMATE_METHODS, max_length=50)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title

    @staticmethod
    def _get_test_name(uid):
        return'test_%s' % uid

    def _get_test_controller(self, id, uid, length):
        return TestControllerRandom(id, uid, length, self)

    def start_test(self, user, duration, length):
        test_log = TestLog.objects.create(
            test=self, user=user)

        cache.set(
            self._get_test_name(test_log.test_uid),
            self._get_test_controller(
                self.id, test_log.test_uid,
                length),
            timeout=duration)
        return test_log

    @classmethod
    def get_test(cls, test_uid):
        return cache.get(
            cls._get_test_name(test_uid))


class AppointedTestQuerySet(models.QuerySet):

    def future(self, **kwargs):
        kwargs['datetime_end__gte'] = timezone.now()

        return self.filter(**kwargs)


class AppointedTestManager(models.Manager):

    def future(self, **kwargs):
        return self.get_queryset().future(**kwargs)

    def get_queryset(self):
        return AppointedTestQuerySet(self.model, using=self._db)


class AppointedTest(models.Model):

    title = models.CharField(
        'Заголовок', default='Назначенный тест', max_length=255)
    users = models.ManyToManyField(User, verbose_name='Пользователи')
    tests = models.ManyToManyField(Test, verbose_name='Тесты')
    duration = models.PositiveSmallIntegerField('Длительность', default=60)
    test_size = models.PositiveSmallIntegerField(
        'Количество вопросов', default=25)
    datetime_start = models.DateTimeField('Начало теста')
    datetime_end = models.DateTimeField('Окончание теста')

    objects = AppointedTestManager()

    class Meta:
        verbose_name = 'Назначенный тест'
        verbose_name_plural = 'Назначенные тесты'

    @property
    def is_available(self):
        now = timezone.now()

        return (
            self.datetime_start <= now and
            self.datetime_end > now)

    def __str__(self):
        return '%s %s-%s' % (
            self.title, self.datetime_start, self.datetime_end)


class AvailableTest(models.Model):

    title = models.CharField(
        'Заголовок', default='Доступный тест', max_length=255)
    users = models.ManyToManyField(User, verbose_name='Пользователи')
    tests = models.ManyToManyField(Test, verbose_name='Тесты')
    test_size = models.PositiveSmallIntegerField(
        'Количество вопросов', default=25)

    class Meta:
        verbose_name = 'Доступный тест'
        verbose_name_plural = 'Доступные тесты'

    def __str__(self):
        return self.title


class TestLog(models.Model):
    test_uid = models.UUIDField(verbose_name="Код теста", default=uuid.uuid4)
    test = models.ForeignKey(Test, verbose_name="Тест", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    datetime_created = models.DateTimeField('Начало теста', auto_now_add=True)
    datetime_completed = models.DateTimeField('Начало теста', blank=True, null=True)
    score = models.PositiveSmallIntegerField('Результат', default=0)

    class Meta:
        verbose_name = 'История тестов'
        verbose_name_plural = 'Истории тестов'

    def __str__(self):
        return '%s %s %s' % self.test.title, self.user.username, self.score
