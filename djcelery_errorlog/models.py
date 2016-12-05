# -*- coding: utf-8 -*-
from functools import wraps
from celery import current_app as celery_app, shared_task as celery_shared_task
from celery.task import periodic_task as celery_periodic_task
from djcelery.picklefield import PickledObjectField
from django.utils import timezone

from django.db import models, transaction
from errorlog.models import BaseError


class CeleryErrorQuerySet(models.QuerySet):

    def fix(self, queue=None):
        for item in self:
            celery_app.send_task(item.task_name, args=item.args, kwargs=item.kwargs, queue=queue)
        self.update(fixed=True, fix_time=timezone.now())


class CeleryError(BaseError):
    objects = models.Manager.from_queryset(CeleryErrorQuerySet)()
    args = PickledObjectField(compress=True)
    kwargs = PickledObjectField(compress=True)
    args_repr = models.TextField(null=True, blank=True)
    kwargs_repr = models.TextField(null=True, blank=True)
    task_name = models.TextField(null=True, blank=True)

    name_property = 'task_name'

    @classmethod
    def from_except(cls, name, tb, exception, args, kwargs, **data):
        return super(CeleryError, cls).from_except(name, tb, exception, args=args, kwargs=kwargs, args_repr=repr(args), kwargs_repr=repr(kwargs), **data)

    @property
    def same_error_items(self):
        return [(item.args, item.kwargs) for item in self.same_errors.only("args", "kwargs")]

    @classmethod
    def shared_task(cls, **options):
        return cls.decorator_factory(celery_shared_task)(**options)

    @classmethod
    def periodic_task(cls, **options):
        return cls.decorator_factory(celery_periodic_task)(**options)

    @classmethod
    def decorator_factory(cls, dec_func):
        def decorator(**options):

            def task_runner_maker(func):
                name = options.get("name") or func.__name__
                bind = options.get("bind", False)
                is_atomic = options.pop("atomic", True)
                func_run = transaction.atomic(func) if is_atomic else func

                @wraps(func)
                def task_runner(*args, **kwargs):
                    save_args = args[1:] if bind else args
                    with cls.log_exception(name, args=save_args, kwargs=kwargs):
                        return func_run(*args, **kwargs)

                task = dec_func(**options)(task_runner)
                task.orig_func = func
                return task
            return task_runner_maker
        return decorator

    def fix(self, queue=None):
        self.same_errors.fix(queue)
