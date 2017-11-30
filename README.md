Zabbix Tools
===========

# zabbix_tool
Tool for CLI interaction with the Zabbix API.

It provides for "simple" CLI access to various Zabbix objects.  It is far
from complete, yet is very useful in it's current state.

# screen_creator

Useful for creating screens in Zabbix.  Can add all of the graphs from a
single host to the screen, as well as adding a single named graph from
every host in a hostgroup.

This uses the zabbix\_api.py from
https://github.com/gescheit/scripts/blob/master/zabbix/zabbix\_api.py.
Someone else has packaged a stale version of that as zabbix\_api in the
Python Cheese Shop, but it's stale.

# Configuration

Each of the above tools expects you to have a config file called ~/.zabbix

The Config file should look like this:
```
-------------- CUT HERE -----------------
[zabbix]
username='zabbix-api-user'
password='not-your-password'
url='http://zabbix-api.example.com/'
validate_certs='True'

[dev]
username='zabbix-dev-api-user'
password='not-mine-either'
url='https://zabbix-dev.example.com/'
validate_certs=''
-------------- CUT HERE -----------------
```

The "zabbix" section is the default used by the scripts, though you can
specify the section to use on the command line.
