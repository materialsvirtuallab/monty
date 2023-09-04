---
layout: default
title: monty.subprocess.md
nav_exclude: true
---

# monty.subprocess module

Calling shell processes.


### _class_ monty.subprocess.Command(command)
Bases: `object`

Enables to run subprocess commands in a different thread with TIMEOUT
option.

Based on jcollado’s solution:

    [http://stackoverflow.com/questions/1191374/subprocess-with-timeout/4825933#4825933](http://stackoverflow.com/questions/1191374/subprocess-with-timeout/4825933#4825933)

and

    [https://gist.github.com/kirpit/1306188](https://gist.github.com/kirpit/1306188)


#### retcode()
Return code of the subprocess


#### killed()
True if subprocess has been killed due to the timeout


#### output()
stdout of the subprocess


#### error()
stderr of the subprocess

### Example

com = Command(“sleep 1”).run(timeout=2)
print(com.retcode, com.killed, com.output, com.output)


* **Parameters**

    **command** – Command to execute



#### run(timeout=None, \*\*kwargs)
Run a command in a separated thread and wait timeout seconds.
kwargs are keyword arguments passed to Popen.

Return: self