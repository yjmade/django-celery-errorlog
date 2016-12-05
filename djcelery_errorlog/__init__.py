# -*- coding: utf-8 -*-
def shared_task(*args, **kwargs):
    from .models import CeleryError
    return CeleryError.shared_task(*args, **kwargs)


def periodic_task(*args, **kwargs):
    from .models import CeleryError
    return CeleryError.periodic_task(*args, **kwargs)
