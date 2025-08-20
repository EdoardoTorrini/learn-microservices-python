from typeguard import typechecked

from random import choice
from datetime import datetime
import pytz


@typechecked
class Noise:

    delay: int = 0
    _zone_id = "Europe/Rome"
    _fault: int = 0

    def fault_exception(self):
        fault = [ 1 for _ in range(self._fault) ]
        ok = [ 0 for _ in range(100 - self._fault)]
        return choice(fault + ok)

    def set_fault(self, fault: int):
        if 0 < fault < 100:
            raise Exception("fault val must be between 0 and 100")
        self._fault = fault

    def get_fault(self) -> int:
        return self._fault
    
    def get_date(self) -> str:
        tz = pytz.timezone(self._zone_id)
        return str(datetime.now(tz).date())
    
    def get_time(self) -> str:
        tz = pytz.timezone(self._zone_id)
        return str(datetime.now(tz).time())
    

noise = Noise()

def get_noise():
    return noise