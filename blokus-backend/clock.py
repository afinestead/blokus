from threading import Timer
from typing import Optional

class Clock:
  def __init__(self, time: Optional[float]):
    self.callback = lambda: print("TODO")
    self._timer = Timer(time, self.callback)

  def start(self):
    pass

  def stop(self):
    pass