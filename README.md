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

This uses the zabbix_api.py from
https://github.com/gescheit/scripts/blob/master/zabbix/zabbix_api.py.
Someone else has packaged a stale version of that as zabbix_api in the
Python Cheese Shop, but it's stale.
