import sched, time

scheduler = sched.scheduler(time.time, time.sleep)


def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)
