import datetime, json, yaml, dict_utils
from typing import List, Dict
from pymongo import MongoClient


class AppInfo:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

DB_SMARTLOG = 'smartlog'
COL_APPS = 'apps'
class MongoLogRepository():
    def __init__(self, connectionStr: str):
        self.client = MongoClient(connectionStr)
        self.appMap : Dict[str, AppInfo] = self.loadApps()
        self.db = self.client[DB_SMARTLOG]

    def loadApps(self):
        try:
            appMap = {}
            query = {'archived': False}
            cursor = self.db[COL_APPS].find(query, sort=[('name',-1)])
            for doc in cursor:
                id = doc['_id']
                name = doc['name']
                appMap[id] = AppInfo(id, name)            
            return appMap
        except Exception as ex:
            print(ex)
            return {}
        
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
                    self.addWorkflowInstance(appid, item)
                else:
                    error = item['error']
                    endTime = item['time']
                    print(f"[Workflow:{wfid}] update instance wiid:{wiid} error={error} endTime={endTime}")
                    wfi['error'] = error
                    wfi['endTime'] = endTime
            else:
                self.addLogEntry(appid, item)

    def addBatchOfWorkflows(self, appid, workflows: List[dict]):
        if appid in self.appMap:
            self.appMap[appid]['workflows'] = dict_utils.appendIfNotExists(workflows, self.appMap[appid]['workflows'])
        else:
            self.appMap[appid] = { 'entries': [], 'workflows': workflows, 'issues': [], 'flows': [] }
        print(yaml.dump(self.appMap[appid]['workflows']))

    def addBatchOfIssues(self, appid, issues: List[dict]):
        if appid in self.appMap:
            self.appMap[appid]['issues'] = dict_utils.appendIfNotExists(issues, self.appMap[appid]['issues'])
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
                for ins in self.appMap[appid]['entries']:
                    if workflowid in ins['tags']:
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