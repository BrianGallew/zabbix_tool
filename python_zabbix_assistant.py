#! /usr/bin/python

import os, json, socket, struct, logging, time, urllib2, platform, threading

# Some day this will use "real" Zabbix auth and become more complicated.
ZABBIX_API_SERVER = 'zabbix-api.example.com'
ZABBIX_KEY = 'xyzzy-plugh-plover'

class ZabbixActiveSender(object):
    '''This will send values to Zabbix via the same mechanism zabbix_sender uses.
    '''
    def __init__(self, zabbixserver=None, prefix = None, no_send=False, clienthost=platform.node()):
        self.lock = threading.Lock()
        self.zabbixserver = zabbixserver
        self.clienthost = clienthost # This better be the FQDN
        logging.debug('ZAS.__init__: clienthost="%s"', self.clienthost)
        self.prefix = prefix
        self.no_send = no_send
        self.check_for_proxy()
        self.clear()
        logging.debug('ZAS.__init__: zabbixserver="%s"', str(self.zabbixserver))
        if os.environ.has_key('http_proxy'): 
            del os.environ['http_proxy']
            logging.debug('ZAS.__init__: removed http_proxy from the environment')
        return

    def check_for_proxy(self):
        '''If the zabbixserver was specified, we trust that (e.g. for
        zabbix-stage.llnw.net).  Otherwise, we go looking for the proxy
        that owns us.
        '''
        if self.zabbixserver: return
        postdata = {
            "key": ZABBIX_KEY,
            "method": "proxymap.get",
            "params": {
                "hostnames": [ os.uname()[1] ],
                "output": "json"
                }
            }
        data = urllib2.urlopen('http://'+ZABBIX_API_SERVER+'/llnw/api_jsonrpc.php',json.dumps(postdata))
        self.zabbixserver = json.load(data)['result'][0]['proxy']
        return

    def __call__(self, key, value):
        '''Load up our dictionary with data preparatory to sending it on to Zabbix.
        If we're debugging, we'll immediately send each value, which makes it a
        *lot* easier to figure out where we've got problems.'''
        logging.debug('ZAS.__call__: %30s\t%s', key, value)
        if self.prefix: key = self.prefix+key
        self.lock.acquire()
        self.data.append({"key":key, "value":value, "host":self.clienthost, "clock":int(time.time())})
        self.lock.release()
        if logging.root.level < logging.INFO: self.send()
        return

    def send(self):
        '''Ship the data to Zabbix.  Call as often as you like, though of course
        it's more efficient to call it just once after you've accumulated
        all of the data you'd like to send.

        The magic in here with structs is required to format everything for
        Zabbix' wire protocol.  If this breaks, it's time to dive into the
        Zabbix internals again.

        '''
        self.lock.acquire()
        if not self.data:
            self.lock.release()
            return # Nothing to send!
        if not self.no_send:
            response = {"request":"agent data", "clock":int(time.time()), "data":self.data}
            string = json.dumps(response)
            logging.debug(string)
            string_to_send = 'ZBXD\x01%s%s' % (struct.pack('<q', len(string)), string)
            s = socket.create_connection((self.zabbixserver, 10051))
            s.sendall(string_to_send)
            s.shutdown(socket.SHUT_WR)
            try:
                retstring = s.recv(5)   # Header, don't care: 'ZBXD\01'
                datalen = struct.unpack('<q',s.recv(8))[0] # Length of data being returned
                retstring = s.recv(datalen)               # Actual return string
                logging.debug(retstring)
            except Exception as e:
                logging.debug('ZAS.send: Failed to get a proper response: %s (%s)', retstring, e)
        self.clear()
        self.lock.release()
        return

    def clear(self): self.data = []
