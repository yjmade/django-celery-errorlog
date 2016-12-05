# -*- coding: utf-8 -*-
from djcelery_errorlog import shared_task


@shared_task(name="tests")
def tests(**kwargs):
    raise ValueError(kwargs)
