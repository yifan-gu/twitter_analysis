#!/usr/bin/python

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *
import struct

def encode(num):
    return struct.pack('>q', num)

def decode(raw):
    return struct.unpack('>q', raw)


class getData():
    """
    get the data from databse
    """
    
    def __init__(self, config):
        """
        init the class, config is the path to the table config file
        """

        f = open(config,'r')
        for line in f.readlines():
            if len(line) > 0:
                self.params[line.split(':')[0]] = line.split(':')[1]
        f.close()
        
        self.transport = TBufferedTransport(TSocket(self.params['address'], int(self.params['port'])))
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.clinet = Hbase.cline(self.protocol)

    def query2(self, ts):
        table = self.params['table_2']
        result = self.client.getRowWithColumns(table, encode(ts), [], {})
        return result

    def query3(self, startId, endId):
        table = self.params['table_3']
        scanner = client.scannerOpenWithScan(table, encode(startId), encode(endId), [], {})
        while (result = client.scannerGet(scanner)):
            print result

    def query4(self, rtid):
        table = self.params['table_4']
        result = self.client.getRowWithColumns(table, encode(rtid), [], {})
        return result
        
        
        
