from threading import Timer


class RepeatTimer(Timer):
    def __init__(self, *args, **kwargs):
        super(RepeatTimer, self).__init__(*args, **kwargs, )
        self.daemon = True

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
