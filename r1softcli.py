# -*- coding: utf-8 -*-

import sys
import suds
 
#-----------------------------------------------
# R1Soft [S]erver [B]ackup [M]anager SOAP Client 
#-----------------------------------------------
class SBMsoapcli(object):
    def __init__(self,**kwargs):
        self.__namespaces = {}
        self.__dict__.update(kwargs)
    def check(self):
        print(self.ipaddr,self.ident,self.cred)
    def __getattr__(self,name):
        ns = self.__namespaces.get(name, None)
        if ns is None:
            ns = suds.client.Client(
                url = 'http://%s:%d/%s?wsdl' % (self.ipaddr,self.port,name),
                username = self.ident,
                password = self.cred
            )
            self.__namespaces[name] = ns
        return ns

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please supply ip address of Idera Server Backup Manager.")
        sys.exit(1)
    ipaddr = sys.argv[1]
    client = SBMsoapcli(
        ipaddr  = ipaddr,
        port    = 9080,
        ident   = 'johnny',
        cred    = 'p4ssw0rd'
    )
    print "Checking backup policies: ",
    failed_policies = []
    count = 0
    for policy in client.Policy2.service.getPolicies():
        count = count + 1
        if policy.state == "ERROR":
            failed_policies.append({'dsid':policy.diskSafeID})
            print "☓",
        else:
            print "✓",
    failed_disksafeids = [ds['dsid'] for ds in failed_policies]
    print "found %d out of %d has backup failure" % (len(failed_policies),count)
    print("Checking for IP Addresses of these failed policies:")
    agents = []
    for agent in client.Agent.service.getAgents():
        agents.append({
            'ipaddr':agent.hostname,
            'id':agent.id,
            'description':agent.description
        })  
    for agent in agents:
        #lfbti = client.Agent.service.getLastFinishedBackupTaskInfo(agent['id'])
        node = client.Agent.service.getAgentByID(agent['id'])
        for disksafe in client.DiskSafe.service.getDiskSafesForAgent(node):
            if disksafe.id in failed_disksafeids:
                print(agent['ipaddr'],agent['description'])
                #print(lfbti)
