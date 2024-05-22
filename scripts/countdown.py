import threading
import arcade
import time
import math

# Increment match duration when a player collects a power-up
class Countdown:
    def __init__(self, match_duration_in_seconds=60):
        self.remaining_time = match_duration_in_seconds
        self.match_duration_in_seconds = match_duration_in_seconds
        self.timer_thread = None
        self.startTime = time.time()

    def start(self):
        self.timer_thread = threading.Thread(target=self._countdown)
        self.timer_thread.start()

    def stop(self):
        if self.timer_thread:
            self.timer_thread.join()
            

    def _countdown(self):
        while self.remaining_time > 0:            
            time.sleep(1)
            self.remaining_time = math.ceil(self.match_duration_in_seconds - (time.time() - self.startTime)) 
                    