# Spanning Tree project for GA Tech OMS-CS CS 6250 Computer Networks
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

from Message import *
from StpSwitch import *


class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)

        # TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        self.root = self.switchID
        self.distance = 0
        self.pathThrough = self.switchID
        self.activeLinks = []

    def send_initial_messages(self):
        # TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        for linkID in self.links:
            # Message(claimedRoot, distanceToRoot, originID, destinationID, pathThrough)
            msg = Message(self.switchID, 0, self.switchID, linkID, False)
            self.send_message(msg)
        return

    def process_message(self, message):
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.

        # Deal with pathThrough.
        if message.pathThrough and message.origin not in self.activeLinks:
            self.activeLinks.append(message.origin)
        elif not message.pathThrough and message.origin != self.pathThrough and message.origin in self.activeLinks:
            self.activeLinks.remove(message.origin)

        # shorter distance found for the same root
        if message.root == self.root and message.distance + 1 < self.distance:
            self. distance = message.distance + 1
            newPathThrough = message.origin
            # notify the change to my neighbors
            for linkID in self.links:
                message = Message(self.root, self.distance, self.switchID, linkID, newPathThrough == linkID)
                self.send_message(message)
            # remove the old pathThrough and update it
            self.activeLinks.remove(self.pathThrough)
            self.pathThrough = newPathThrough
            if newPathThrough not in self.activeLinks:
                self.activeLinks.append(newPathThrough)

        # same distance and same root but a smaller switchID
        if message.root == self.root and message.distance + 1 == self.distance and self.pathThrough > message.origin:
            newPathThrough = message.origin

            for linkID in self.links:
                message = Message(self.root, self.distance, self.switchID, linkID, newPathThrough == linkID)
                self.send_message(message)

            self.activeLinks.remove(self.pathThrough)
            self.pathThrough = newPathThrough
            if newPathThrough not in self.activeLinks:
                self.activeLinks.append(newPathThrough)

        # change of root
        if message.root < self.root:
            self.root = message.root
            self.distance = message.distance + 1
            self.pathThrough = message.origin
            if self.pathThrough not in self.activeLinks:
                self.activeLinks.append(self.pathThrough)
            # send messages to my neighbors
            for linkID in self.links:
                message = Message(self.root, self.distance, self.switchID, linkID, self.pathThrough == linkID)
                self.send_message(message)

        return



    def generate_logstring(self):
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        links = []
        self.activeLinks.sort()
        for linkID in self.activeLinks:
            links.append(str(self.switchID) + ' - ' + str(linkID))
        return ', '.join(links)