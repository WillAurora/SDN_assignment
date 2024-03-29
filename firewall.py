'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

import csv


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''

class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")
        self.deny = []
        with open(policyFile, 'rb') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.deny.append((EthAddr(row['mac_0']), EthAddr(row['mac_1'])))
                self.deny.append((EthAddr(row['mac_1']), EthAddr(row['mac_0'])))

    def _handle_ConnectionUp (self, event):    
        for (src, dst) in self.deny:
            match = of.ofp_match() #  an of class
            match.dl_src = src
            match.dl_dst = dst
            msg = of.ofp_flow_mod() # an of class
            msg.match = match # construct a message with match
            event.connection.send(msg)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))


def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
