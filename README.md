# smartlog-server-fastapi
smart log server using fastapi


# install
pip3 install fastapi python-devenv


# Models

## Worklfow

```yaml
id: 
name: 
category:
```

## Workflow Instance:

```yaml
wfid: workflow id
wiid: workflow instance id
error: str
endTime: datetime
```

## Log Entry
```yaml
tags:
time: datetime
msg: 
v:
```
