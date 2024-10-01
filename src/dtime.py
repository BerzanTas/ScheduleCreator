class Time:
    """Simple time module, where you can define hour and minute.
    You can perform adding and substracting operations on it.
    """
    def __init__(self, hour:int=0, minute:int=0) -> None:
        self.hour = hour
        self.minute = minute
    
    def __str__(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d}"
    
    def __repr__(self) -> str:
        return f"Time({self.hour}, {self.minute})"
    
    def __add__(self, other: object) -> object:
        if isinstance(other, Time):
            return Time(self.hour + other.hour, self.minute + other.minute)
        return NotImplemented
    
    def __sub__(self, other: object) -> object:
        if isinstance(other, Time):
            return Time(self.hour - other.hour, self.minute - other.minute)
        return NotImplemented
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Time):
            return (self.hour == other.hour and self.minute == other.minute)
        else:
            return NotImplemented
    
    def __ne__(self, other: object) -> bool:
        if isinstance(other, Time):
            return (self.hour != other.hour or self.minute != other.minute)
        else:
            return NotImplemented
    
    def __lt__(self, other: object) -> bool:
        if isinstance(other, Time):
            if self.hour != other.hour:
                return self.hour < other.hour
            else:
                return self.minute < other.minute
        else:
            return NotImplemented
    
    def __le__(self, other: object) -> bool:
        if isinstance(other, Time):
            if self.hour < other.hour:
                return True
            elif self.hour == other.hour:
                return self.minute <= other.minute
            else:
                return False
        else:
            return NotImplemented
        
    def __gt__(self, other: object) -> bool:
        if isinstance(other, Time):
            if self.hour != other.hour:
                return self.hour > other.hour
            else:
                return self.minute > other.minute
        else:
            return NotImplemented
        
    def __ge__(self, other: object) -> bool:
        if isinstance(other, Time):
            if self.hour > other.hour:
                return True
            elif self.hour == other.hour:
                return self.minute >= other.minute
            else:
                return False
        else:
            return NotImplemented
        
    def __hash__(self) -> int:
        return hash((self.hour, self.minute))
    
    @property
    def hour(self):
        return self._hour
    
    @hour.setter
    def hour(self, value):
        self._hour = value%24
    
    @property
    def minute(self):
        return self._minute
    
    @minute.setter
    def minute(self, value):
        self._minute = value%60
    