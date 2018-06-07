from RandVar import RandVar as RV
from collections import deque

class MM1:

    def __init__(self, process_rate, warmup_time, record_time):

        self.running = False
        self.process_rate = process_rate
        self.departure_time = 0
        self.total_runtime = 0
        self.warmup_time = warmup_time
        self.record_time = record_time
        self.queue = deque([])
        self.task = 0
        self.old_t = warmup_time
        self.w = 0
        self.q = 0
        self.Tw = 0
        self.Tq = 0

    def query(self, t, item):
        '''Query the system with the current time and a boolean value which indicate
        whether an event is arriving return next departure time if the system is running
        or set departure time to an arbitrarily large number if the system
        is idle'''

        #Keep track of items in queue and system for w and q
        if t > self.warmup_time:

            self.w += (t - self.old_t) * len(self.queue)
            self.q += (t - self.old_t) * (len(self.queue) + self.running)

            self.old_t = t

        #Pass item into the queue if an item is incoming
        if item:
            self.queue.append(t)

        #Pass new item into system if it finished previous event or idling
        if self.departure_time == t or not self.running:
            
            if self.queue:

                self.running = True
                t_in = self.queue.popleft()
                t_out = self.run_time(t)
    
                #Keep track of runtime of items in system for Tw and Tq
                if t > self.warmup_time:
            
                    self.total_runtime += t_out
                    self.task += 1
                    self.Tw += (t - t_in)
                    self.Tq += (t - t_in) + t_out

                #Return departure time
                return t + t_out

            else:

                #Set departure time to an arbitrarily large number if the system
                # is idle
                self.running = False
                return self.warmup_time + self.record_time + 10

        return self.departure_time

    def run_time(self, t):
        '''Get run time from RandVar'''
        time = RV.exp(self.process_rate)
        self.departure_time = t + time

        return time

    def __str__(self):

        rho = "rho = " + str(self.total_runtime / self.record_time)
        q = "q = " + str(self.q / self.record_time)
        Tq = "Tq = " + str(self.Tq / self.task)
        w = "w = " + str(self.w / self.record_time)
        Tw = "Tw = " + str(self.Tw / self.task)
        Ts = "Ts = " + str(self.total_runtime / self.task)
        '''For 4 d) and f)
        Throughput = "Throughput = " + str(self.task / self.record_time)
        '''
        return rho + "\n" + q + "\n" + Tq + "\n" + w + "\n" + Tw + "\n" + Ts #+ "\n" + Throughput
