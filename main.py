# -*- coding: utf-8 -*-
import atexit
from webapp import app
from apscheduler.schedulers.background import BackgroundScheduler

import parsing


def timed_job():
    parsing.do()
sched = BackgroundScheduler()
sched.add_job(func=timed_job, trigger="interval", hours=6)
sched.start()


def main():
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
    atexit.register(lambda: sched.shutdown())


if __name__ == "__main__":
    main()
