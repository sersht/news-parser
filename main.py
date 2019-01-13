# -*- coding: utf-8 -*-
import atexit
from webapp import app
from apscheduler.schedulers.background import BackgroundScheduler

import tsnua
import ukrnet


sched = BackgroundScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    ukrnet.parse()
    tsnua.parse()

sched.start()


def main():
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
    atexit.register(lambda: sched.shutdown())


if __name__ == "__main__":
    main()
