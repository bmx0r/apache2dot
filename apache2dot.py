#get a apache config file from the stdin and output a dot file


import sys
import re
import pydot
with open('vhost.conf', 'r') as f:
    read_data = f.read()

listVhost = []

patternBalance = re.compile(r'.*?(BalancerMember) (.*?)$',re.M|re.I|re.S)
patternVhost = re.compile(r'^\<VirtualHost (.*?)\>$',re.M|re.I|re.S)
getFullVhost = re.compile(r'^\<VirtualHost (.*?)\>(.*?)\<\/VirtualHost\>$',re.M|re.I|re.S)

for item in getFullVhost.findall(read_data):
    vhost = {}
    vhost['name'] = item[0]
    listBall = []
    for i in patternBalance.findall(item[1]):
        listBall.append(i[1])
    vhost['BalancerMember'] = listBall
    listVhost.append(vhost)


Mygraph = pydot.Dot(graph_name='G', graph_type='digraph',
                strict=False, suppress_disconnected=False)
for vhost in listVhost:
    Myvhost = pydot.Node(vhost['name'], label=vhost['name'])
    Myvhost.set_name(vhost['name'])
    Mygraph.add_node(Myvhost )
    for backend in vhost['BalancerMember']:
        Mybackend = pydot.Node(backend, label=backend)
        Mybackend.set_name(backend)
        Mygraph.add_node(Mybackend)
        Mygraph.add_edge(pydot.Edge(Myvhost,Mybackend))


print Mygraph.to_string()
Mygraph.create(prog='dot', format='ps')

