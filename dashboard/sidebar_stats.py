class sidebar_stats:
    def __init__(self,limit:int = 5,days:int = 30):
        self.limit = limit
        self.days = days
        pass

    def set_limit(self,limit:int):
        self.limit = limit
    def set_days(self,days:int):
        self.days = days

    def get_limit(self):
        return self.limit
    def get_days(self):
        return self.days    