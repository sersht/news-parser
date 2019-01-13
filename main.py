# -*- coding: utf-8 -*-
import atexit
from webapp import app
from apscheduler.schedulers.background import BackgroundScheduler

import tsnua
import ukrnet


def timed_job():
    ukrnet.parse()
    tsnua.parse()


sched = BackgroundScheduler()
sched.add_job(func=timed_job, trigger="interval", seconds=5)
sched.start()


def main():
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
    atexit.register(lambda: sched.shutdown())


if __name__ == "__main__":
    main()
