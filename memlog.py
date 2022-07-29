class MemoryLogRepository():
    def __init__(self) -> None:
        self.appMap = {}

    def addAll(self, appid, batch):
        if appid in self.appMap:
            self.appMap[appid] = self.appMap[appid] + batch
        else:
            self.appMap[appid] = batch

    def getAppLog(self, appid):
        if appid in self.appMap:
            return self.appMap[appid]
        return []