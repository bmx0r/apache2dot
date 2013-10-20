import csv
import pygraphviz as pgv


#samplerecord
#aerobix.unix.banksys.be|4AS|Actif|eth2|'00:18:fe:87:51:f0|'192.168.2.2|'255.255.255.0|192.168.2.0/24|

listNetwork = set()
ignoredNet =[ "",
	      "127.0.0.1/32",
	      "192.168.2.0/24",
	      "192.168.3.0/24",
	      "192.168.4.0/24",
	      "192.168.5.0/24",
	      "192.168.0.0/23",
 	      "192.168.0.0/29",
	      "192.168.0.0/30",
	      "192.168.1.0/24",
	      "192.168.226.0/23",
	      "192.168.231.0/24",
	      "192.168.244.0/22",
	      "192.168.0.0/23",
"192.168.0.0/29",
"192.168.0.0/30",
"192.168.1.0/24",
"192.168.122.0/24",
"192.168.140.192/27",
"192.168.192.0/24",
"192.168.194.0/26",
"192.168.195.160/27",
"192.168.2.0/24",
"192.168.200.0/26",
"192.168.201.160/27",
"192.168.205.128/27",
"192.168.226.0/23",
"192.168.231.0/24",
"192.168.232.0/24",
"192.168.240.0/22",
"192.168.240.0/24",
"192.168.244.0/22",
"192.168.244.0/24",
"192.168.244.1/32",
"192.168.244.10/32",
"192.168.244.3/32",
"192.168.244.59/32",
"192.168.244.61/32",
"192.168.244.63/32",
"192.168.244.69/32",
"192.168.244.90/32",
"192.168.244.91/32",
"192.168.248.0/24",
"192.168.249.0/24",
"192.168.255.0/24",
"192.168.255.128/25",
"192.168.255.158/32",
"192.168.255.159/32",
"192.168.255.16/29",
"192.168.255.161/32",
"192.168.255.162/32",
"192.168.255.163/32",
"192.168.255.244/32",
"192.168.255.64/28",
"192.168.255.80/28",
"192.168.3.0/24",
"192.168.4.0/24",
"192.168.5.0/24",
"192.168.50.128/26",
"192.168.50.32/27",
"192.168.50.64/27",
"192.168.56.128/26",
"192.168.56.32/27",
"169.254.0.0/16",
	    ]
listHost =[]
G=pgv.AGraph(strict='true')
G.graph_attr.update(rankdir="LR",ranksep='1',splines='line')
#G.graph_attr['outputorder']='edgesfirst'
G.graph_attr['overlap']='false'


#G.node_attr['style']='filled'
#G.node_attr['shape']='circle'
#G.node_attr['fontcolor']='#FFFFFF'
G.node_attr['fontsize']='8'



class Interface(object):
	def __init__(self,mac,name,ip,mask,network):
		self.mac=mac
		self.name=name
		self.ip=ip
		self.mask=mask
		self.network=network
		self._add_to_netlist()
	
	def _add_to_netlist(self):
		""""""
		if self.is_valid_network():
			listNetwork.add(self.network)

	def is_valid_network(self):
		rc=True
		if self.network in ignoredNet:
			rc=False
		return rc

	def __repr__(self):
		return "{0}".format(self.mac)

class Host(object):
	def __init__(self,hostname=None,os=None):
		self.hostname=hostname
		self.os=os
		self.interfaces=[]

	def add_interface(self,interface):
		self.interfaces.append(interface)
	
	def __repr__(self):
		return "{0}".format(self.hostname)

with open('LINUX_TCPIPADD_ALL.csv', 'rb') as csvfile:
    #iplist = csv.reader(csvfile, delimiter='|', quotechar='\'')
    iplist = csv.reader(csvfile, delimiter='|')
    iflist = []
    hostname = ""
    host = None
    for row in iplist:
        if hostname != row[0]:
            if host:
                listHost.append(host)
                del host
            hostname = row[0]
            host = Host(row[0],row[1])
	eth = Interface(row[4],row[3],row[5],row[6],row[7])
        host.add_interface(eth)

for item in sorted(listNetwork):
    G.add_node(item)
    tbl= [item]
    B=G.add_subgraph(item, name="cluster_%s" %item,rank='same')
    n=G.get_node(item)
    n.attr['shape']="box3d"

for item in sorted(listHost, key=lambda host: host.hostname) :
    tbl= [item]
#    G.add_subgraph(tbl, name="cluster_%s" %item,rank='same')
#    G.add_node(item)
    for eth in item.interfaces:
        if eth.is_valid_network():
#        if "172.18.231.0" in eth.network:
            G.add_subgraph(tbl, name="cluster_%s" %eth.network,rank='same')
            G.add_edge(item,eth.network,constraint='false')

#

G.write("file.dot")
G.layout()
#G.draw('file.dot.png',prog='dot') 
#G.draw('file.neato.png',prog='neato') 
G.draw('file.twopi.png',prog='twopi') 
G.draw('file.sfdp.png',prog='sfdp') 
