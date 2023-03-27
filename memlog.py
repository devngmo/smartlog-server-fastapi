import datetime, json
from typing import List


def appendIfNotExists(src:List[dict], dest:List[dict]):
    for s in src:
        d = [x for x in dest if x['id'] == s['id']]
        if len(d) == 1:
            continue
        else:
            print(f"add {json.dumps(s)}")
            dest += [s]
    return dest
class MemoryLogRepository():
    def __init__(self) -> None:
        self.appMap = {}


    def addBatchOfLogs(self, appid, entries:List[dict]):
        for item in entries:
            if not 'time' in item:
                item['time'] = datetime.datetime.now()

        if appid in self.appMap:
            self.appMap[appid]['entries'] += entries
        else:
            self.appMap[appid] = { 'entries': entries, 'workflows': [], 'issues': [] }

    def addBatchOfWorkflows(self, appid, workflows: List[dict]):
        if appid in self.appMap:
            self.appMap[appid]['workflows'] = appendIfNotExists(workflows, self.appMap[appid]['workflows'])
        else:
            self.appMap[appid] = { 'entries': [], 'workflows': workflows, 'issues': [] }

    def addBatchOfIssues(self, appid, issues: List[dict]):
        if appid in self.appMap:
            self.appMap[appid]['issues'] = appendIfNotExists(issues, self.appMap[appid]['issues'])
        else:
            self.appMap[appid] = { 'entries': [], 'workflows': [], 'issues': issues }


    def clearAppLog(self, appid):
        if appid in self.appMap:
            self.appMap[appid]['entries'] = []

    def getAppLog(self, appid):
        if appid in self.appMap:
            return self.appMap[appid]['entries']
        return []

    def getAppWorkflows(self, appid):
        if appid in self.appMap:
            return self.appMap[appid]['workflows']
        return []

    def getAppIssues(self, appid):
        if appid in self.appMap:
            return self.appMap[appid]['issues']
        return []