import os
from datetime import timedelta, datetime
from contextlib import contextmanager
from django.core.cache import cache

@contextmanager
def task_lock(lock_id, oid, lock_expire_seconds=600, unlock_after_finish=False):
    """
    Be sure that task runs only once
    :param lock_id: unique id of task
    :param oid: unique id of current job (needs for debug only)
    :param lock_expire_seconds: task will be unlocked in x seconds
    :param unlock_after_finish: bool, allow run next task after finish of current one
    """
    timeout_at = datetime.utcnow() + timedelta(seconds=lock_expire_seconds)
    oid = "{}-{}".format(os.environ.get("HOSTNAME", ""), oid)
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, lock_expire_seconds)
    try:
        yield status
    finally:
        # cache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if unlock_after_finish and datetime.utcnow() < timeout_at:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else.
            cache.delete(lock_id)