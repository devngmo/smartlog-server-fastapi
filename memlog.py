import datetime
from typing import List

class MemoryLogRepository():
    def __init__(self) -> None:
        self.appMap = {}

    def addAll(self, appid, batch:List[dict]):
        for item in batch:
            if not 'time' in item:
                item['time'] = datetime.datetime.now()

        if appid in self.appMap:
            self.appMap[appid] = self.appMap[appid] + batch
        else:
            self.appMap[appid] = batch

    def getAppLog(self, appid):
        if appid in self.appMap:
            return self.appMap[appid]
        return []