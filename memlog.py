import datetime, json, yaml
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

    def getWorkflowInstance(self, appid: str, workflowid: str, wiid: str):
        if appid in self.appMap == False:
            return None
        for f in self.appMap[appid]['flows']:
            if f['wfid'] == workflowid and f['wiid'] == wiid:
                return f
        return None


    def addWorkflowInstance(self, appid: str, item: dict):
        if 'endTime' in item == False:
            item['endTime'] = None
        if appid in self.appMap:
            self.appMap[appid]['flows'] += [item]
        else:
            self.appMap[appid] = { 'entries': [], 'workflows': [], 'issues': [], 'flows': [item] }

    def addLogEntry(self, appid: str, entry: dict):
        if appid in self.appMap:
            self.appMap[appid]['entries'] += [entry]
        else:
            self.appMap[appid] = { 'entries': [entry], 'workflows': [], 'issues': [], 'flows': [] }
        
    def addBatchOfLogs(self, appid, entries:List[dict]):
        for item in entries:
            if not 'time' in item:
                item['time'] = datetime.datetime.now()
            else:
                item['time'] = datetime.datetime.fromisoformat(item['time'])
            if 'wfid' in item:
                wfid = item['wfid']
                wiid = item['wiid']
                wfi = self.getWorkflowInstance(appid, wfid, wiid)
                if wfi == None:
                    print(f'[Workflow:{wfid}] add instance wiid:{wiid}')
                    wfi = {'error': None, 'time': item['time'], 'endTime': None, 'wfid': wfid, 'wiid': wiid}
                    self.addWorkflowInstance(appid, wfi)
                else:
                    error = None
                    if 'error' in item:
                        error = item['error']

                    endTime = item['time']
                    print(f"[Workflow:{wfid}] update instance wiid:{wiid} error={error} endTime={endTime}")
                    if error != None and ('error' not in wfi or wfi['error'] == None):
                        wfi['error'] = error
                    wfi['endTime'] = endTime
            
            self.addLogEntry(appid, item)

    def addBatchOfWorkflows(self, appid, workflows: List[dict]):
        if appid in self.appMap:
            self.appMap[appid]['workflows'] = appendIfNotExists(workflows, self.appMap[appid]['workflows'])
        else:
            self.appMap[appid] = { 'entries': [], 'workflows': workflows, 'issues': [], 'flows': [] }
        print(yaml.dump(self.appMap[appid]['workflows']))

    def addBatchOfIssues(self, appid, issues: List[dict]):
        if appid in self.appMap:
            self.appMap[appid]['issues'] = appendIfNotExists(issues, self.appMap[appid]['issues'])
        else:
            self.appMap[appid] = { 'entries': [], 'workflows': [], 'issues': issues, 'flows': [] }


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

    def filterFlow(self, appid: str, workflowid: str):
        print(f"[{appid}] filterFlow: {workflowid}:")
        ls = []
        if appid in self.appMap:
            for ins in self.appMap[appid]['flows']:
                print(ins)
                if ins['wfid'] == workflowid:
                    ls += [ins]
        return ls
    
    def getFlowLogs(self, appid: str, workflowid: str, wiid: str, includeNonFlowLogs = False):
        print(f"[{appid}] getFlowLogs: {workflowid}/{wiid}:")
        ls = []
        if appid in self.appMap:
            wfi = self.getWorkflowInstance(appid, workflowid, wiid)
            if wfi != None:
                wfiStart = wfi['time']
                wfiEnd = wfi['endTime']
                for ins in self.appMap[appid]['entries']:
                    if workflowid in ins['tags']:
                        if ins['time'] >= wfiStart:
                            if wfiEnd == None or ins['time'] <= wfiEnd:
                                ls += [ins]
                    elif includeNonFlowLogs:
                        if ins['time'] >= wfi['time']:
                            if wfi['endTime'] == None:
                                ls += [ins]
                            else:
                                if wfi['endTime'] >= ins['time']:
                                    ls += [ins]
                                else:
                                    break
        return ls


    def getAppIssues(self, appid):
        if appid in self.appMap:
            return self.appMap[appid]['issues']
        return []