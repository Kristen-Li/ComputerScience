# Distance Vector project for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, Jeffrey Randow, new VM fixes by Jared Scott and James Lohse.

from Node import *
from helpers import *


class DistanceVector(Node):

    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """ Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)

        # TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data
        self.vector = {}
        self.vector[name] = 0

    def send_initial_messages(self):
        """ This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight """

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        for incoming_link in self.incoming_links:
            # message format : (origin node, origin node distance vector)
            msg = (self.name, self.vector.copy())
            self.send_msg(msg, incoming_link.name)

    def process_BF(self):
        """ This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. """

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages
        # mark the cases when valid DV changes are made
        update = False
        
        for msg in self.messages:
            node_origin = msg[0]
            node_weights = msg[1]
            for node_name, node_weight in node_weights.items():
                self_to_mid = int(self.get_outgoing_neighbor_weight(node_origin))
                mid_to_node = int(node_weight)
                new_weight = self_to_mid + mid_to_node
                if node_name not in self.vector and node_name != self.name:
                    self.vector[node_name] = new_weight
                    update = True
                elif node_name in self.vector and node_name != self.name:
                    if self.vector[node_name] == -99:
                        continue
                    # if any path is -99, need to set the new distance to -99
                    elif self_to_mid <=-99 or mid_to_node <= -99 or new_weight <= -99:
                        self.vector[node_name] = -99
                        update = True
                    elif new_weight < self.vector[node_name] and new_weight > -99:
                        self.vector[node_name] = new_weight
                        update = True
        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances
        # send messages only when changes are made
        if update:
            msg = (self.name,self.vector.copy())
            for incoming_link in self.incoming_links:
                self.send_msg(msg, incoming_link.name)
        return

    def log_distances(self):
        """ This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 """

        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.        
        vec_string = ",".join("{}{}".format(i, j) for i, j in self.vector.items())
        add_entry(self.name, vec_string)
