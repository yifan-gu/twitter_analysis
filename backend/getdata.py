#!/usr/bin/python

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *
import struct
import json

def encode(num):
    return struct.pack('>q', num)

def decode(raw):
    return struct.unpack('>q', raw)[0]

class getdata():
    """
    get the data from databse
    """
    
    def __init__(self, config):
        """
	    print (i.split(':')[1])
        init the class, config is the path to the table config file
        """

        self.params = {}
        f = open(config,'r')
        for line in f.readlines():
            if len(line) > 1: # 1 for \n
                self.params[line.split(':')[0]] = line.split(':')[1][:-1]
        f.close()
        
        self.transport = TBufferedTransport(TSocket(self.params['address'], int(self.params['port'])))
        self.transport.open()
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Hbase.Client(self.protocol)

    def query2(self, ts):
        table = self.params['table_2']
        result = self.client.getRowWithColumns(table, encode(ts), [], {})
	#print result
	if len(result) <= 0:
	    return []
	
	tw = []
	cols = {}
	#print result[0].columns.keys()
	
	for i in result[0].columns:
	    cols[decode(i[len('ut:'):])] = result[0].columns[i].value	
	for i in sorted(cols.keys()):
	    #print repr(cols[i].decode('utf-8'))[2:]
	    tw.append(str(i)+':'+ json.dumps(cols[i].decode('utf-8'))[1:-1].replace('/', '\\/'))
	    #tw.append(str(i)+':'+ repr(cols[i].decode('utf-8'))[2:-1].replace('\\\'', '\''))
        return tw

    def query3(self, startId, endId):
        table = self.params['table_3']
	cnt = 0
        scanner = self.client.scannerOpenWithStop(table, encode(startId), encode(endId+1), [], {})
        result = self.client.scannerGet(scanner)
        while (len(result) > 0):
	    cnt = cnt + len(result[0].columns)
            #print result
            result = self.client.scannerGet(scanner)
	self.client.scannerClose(scanner)

	return cnt

    def query4(self, rtid):
        table = self.params['table_4']
	#print 'try get'
        result = self.client.getRowWithColumns(table, encode(rtid), [], {})
	if len(result) <= 0:
	    return []

	usr = []
	#print result[0].columns
	for i in result[0].columns:
	    usr.append(decode(i[len('usr:'):]))
	        #print decode(i.split(':')[1])
	    #usr.append(i['usr'])print i
        return usr
        
if __name__ == '__main__':
    a = getdata('table_config.txt')
    r = a.query2(1380644973)
    print r
