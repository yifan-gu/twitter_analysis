#!/usr/bin/python

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *
import struct

#a = u'\u4f60'.encode('utf8')
#print a

transport = TBufferedTransport(TSocket('localhost', 9090))
transport.open()
protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = Hbase.Client(protocol)

#print dir(client)

l = client.getTableNames()

#print l


table = 'test'

#scan = TScan()
#
#scan.filterString = 'SingleColumnValueFilter(\'cf\', \'a\', =, \'binary:\xe3\x80\x90\xe3\x81\x8b\xe3\x82\x8f\xe3\x81\x84\xe3\x81\x99\xe3\x81\x8e\xe3\x82\x8b\xe3\x80\x91\', true, false)'
#
##scan.filterString = 'SingleColumnValueFilter(\'cf\', \'a\', >, \'binary:3\', true, false)'
#
#scanner = client.scannerOpenWithScan(table, scan, {})
#
#result = client.scannerGet(scanner)
#while result:
#	print result
#	result = client.scannerGet(scanner)


#scanner2 = client.scannerOpenWithScan(table, scan, {})
#
#result = client.scannerGet(scanner2)
#print 'result'
#print result
#while result:
#	print result
#	result = client.scannerGet(scanner2)


l = client.getRowWithColumns(table, '\x00\x00\x00\x7b', ['ccf:'], {})
#print l[0].columns

a = struct.pack('>i', 23)
b = struct.pack('>i', 44)
#print a
scanner = client.scannerOpenWithStop('test', a, b, [], {})

#result = client.scannerGet(scanner)
while (result = client.scannerGet(scanner)):
        print struct.unpack('>i',result[0].row)[0]
        #result = client.scannerGet(scanner)

client.scannerClose(scanner)
