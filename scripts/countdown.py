import threading
import time
import math

class Countdown:
    def __init__(self, match_duration_in_seconds=60):
        self.remaining_time = match_duration_in_seconds
        self.match_duration_in_seconds = match_duration_in_seconds
        self.remaining_time_string = self._format_time(self.remaining_time)
        self.timer_thread = None
        self.start_time = time.time()
        self.time_added = 0

    def start(self):
        self.timer_thread = threading.Thread(target=self._countdown)
        self.timer_thread.start()

    def stop(self):
        if self.timer_thread:
            self.timer_thread.join()
            
    def increase_time(self, time_increase):
        self.time_added += time_increase
    
    def get_complete_match_duration(self):
        return self.match_duration_in_seconds + self.time_added
            
    def _countdown(self):
        while self.remaining_time > 0:
            time.sleep(1)
            
            time_since_last_check = time.time() - (self.start_time + self.time_added) 
            
            self.remaining_time = math.ceil(
                self.match_duration_in_seconds + self.time_added - time_since_last_check
            )
            
            self.remaining_time_string = self._format_time(self.remaining_time)
    
    def _format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
        
        
                    