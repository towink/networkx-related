# -*- coding: utf-8 -*-
#    Copyright (C) 2018 by
#    Marta Grobelna <marta.grobelna@rwth-aachen.de>
#    Petre Petrov <petrepp4@gmail.com>
#    Rudi Floren <rudi.floren@gmail.com>
#    Tobias Winkler <tobias.winkler1@rwth-aachen.de>
#    All rights reserved.
#    BSD license.
#
# Authors:  Marta Grobelna <marta.grobelna@rwth-aachen.de>
#           Petre Petrov <petrepp4@gmail.com>
#           Rudi Floren <rudi.floren@gmail.com>
#           Tobias Winkler <tobias.winkler1@rwth-aachen.de>

"""This class is needed for transformation of a Boltzmann sampler for bicolored binary trees
into a Boltzmann sampler for 3-connected planar graphs.
"""
##################################################################
#  THIS IS BASED ON THE PAPER "DISSECTIONS AND TREES, WITH WITH  #
#  APPLICATIONS TO OPTIMAL MESH ENCODING AND TO RANDOM SAMPLING" #
##################################################################

import networkx as nx
from .binary_tree import BinaryTreeSampler
from .halfedge import HalfEdge

class Closure:   

    #Convert a binary tree int o planar map
    def ___btree_to_planar_map(btree):
        init_half_edge = HalfEdge()
        construct_planar_map(btree, init_half_edge)
        #Destroy the initial half-edge as it is only needed to construct its opposite
        init_half_edge.opposite.opposite = None
        return init_half_edge.opposite



    #Consturct planer map out of a binary tree, i.e., make the binary tree
    #tri-oriented
    def ___construct_planar_map(btree, init_half_edge):
        half_edge_1 = HalfEdge()
        half_edge_2 = HalfEdge()
        half_edge_3 = HalfEdge()

        half_edge_1.opposite = init_half_edge
        init_half_edge.opposite = half_edge_1
        
        #Next edge is the one in ccw order around the incident vertex
        half_edge_1.next = half_edge_2
        half_edge_2.next = half_edge_3
        half_edge_3.next = half_edge_1
        
        #Prior edge is the one in cw order around the incident vertex
        half_edge_1.prior = half_edge_3
        half_edge_3.prior = half_edge_2
        half_edge_2.prior = half_edge_1

        #Set the colors of the half-edges
        color = btree.attr['color']
        half_edge_1.color = color
        half_edge_2.color = color
        half_edge_2.color = color


        #Construct the planar map on the children
        if btree.left_child != None:
            return construct_planar_map(btree.left_child, half_edge_2)
        if btree.right_child != None:
            return construct_planar_map(btree.right_child, half_edge_3)



    #Performs bicolored partial closure on a binary tree. When possible build
    #new edges in order to get faces with 4 edges
    #Input: initial half-edge, an empty stack that will contain unpaired half-edges
    #and the color of the initial node
    def ___bicolored_partial_closure(init_half_edge):
        break_half_edge = init_half_edge
        #Travelse the tree in ccw order
        while True:
            current_half_edge = current_half_edge.next
            #Check if the incident vertex is a leaf
            if current_half_edge.opposite == None:
                #It is a leaf
                if len(stack) == 0:
                    #We have to remember the first stem in order to break the loop
                    break_half_edge = current_half_edge
                else:
                    if current_half_edge == break_half_edge:
                        #We finished the closure
                        break
                #The edge has to be stored in our stack in order to find a opposite for it
                stack.append(current_half_edge)
            else:
                #It is a node and its opposite incident vertex must be of the opposite color
                current_half_edge = current_half_edge.opposite
                if len(stack) != 0:
                    last_visited_steam = stack.pop()
                    last_visited_steam.number_proximate_inner_edges += 1
                    #If the steam is followed by three inner edges we can perform local closure
                    if last_visited_steam.number_proximate_inner_edges == 3:
                        steam_opposite = HalfEdge()
                        
                        last_visited_steam.opposite = steam_opposite
                        steam_opposite.opposite = last_visited_steam
                        
                        #Set pointers of the new half-edge
                        steam_opposite.prior = current_half_edge
                        steam_opposite.next = current_half_edge.next
                        
                        #Update the pointer of the old edges
                        current_half_edge.next = steam_opposite
                        current_half_edge.next.prior = steam_opposite

                        stack.pop()
                        #Next half-edge to check is the one prior to our former stem
                        current_half_edge = last_visited_steam.prior
                            
        return break_half_edge



    #Performs bicolored complete closure on a planar map of a binary tree in order to obtain
    #a dissection of the hexagon with quadrangular faces
    #input: init_half_edge is the half-edge that we get when we convert a binary tree into
    #a planar map
    def ___bicolored_complete_closure(init_half_edge):

        starting_half_edge = ___bicolored_partial_closure(init_half_edge)
        hexagon = [HalfEdge() for i in range(12)]
        hexagon_start_half_edge = ___construct_hexagon(hexagon, starting_half_edge.color)

        #Connect the starting half-edge of our planar map with the first node of the hexagon
        new_half_edge = HalfEdge()
        starting_half_edge.opposite = new_half_edge
        new_half_edge.next = hexagon_start_half_edge
        hexagon_start_half_edge.prior = new_half_edge
        hexagon[11].next = new_half_edge
        new_half_edge.prior = hexagon[11]

        #Now traverse the planar map. Depending on the distance between a new inner edge and
        #the next half-edge one can assign the new half edge to a certain hexagon node
        distance = 0
        hexagon_iter = 0
        current_half_edge = starting_half_edge
        while True:
            current_half_edge = current_half_edge.next

            if current_half_edge == starting_half_edge:
                #We are finished as we are back again at our starting half-edge
                break
            
            if current_half_edge == None:
                #We have a stem

                if distance > 2:
                    print("ERROR: distance is greater than 2 -> local closure was possible!")
                    break
                if distance == 0:
                    #In order to get faces having 4 edges we have to assign this half-edge to the 
                    #node 2 nodes further then our hexagon iterator is pointing now
                    hexagon_iter += 4

                if distance == 1:
                    #This half-edge has to be assigned to the node 1 node further
                    hexagon_iter += 2

                #If distance is equal 2 then we have to stay at current hexagon node

                fresh_half_edge = HalfEdge()
                current_half_edge.opposite = fresh_half_edge
                fresh_half_edge.opposite = current_half_edge

                fresh_half_edge.next = hexagon[hexagon_iter-1]
                fresh_half_edge.prior = hexagon[hexagon_iter]
                hexagon[hexagon_iter-1].prior = fresh_half_edge
                hexagon[hexagon_iter].next = fresh_half_edge

            else:
                distance += 1
        #TODO: Check which one to return
        return hexagon[0]


    #Constructs a hexagon out of a list of half_edges. The color argument defines the color of the
    #first half-edge of the hexagon
    def ___construct_hexagon(hexagon_half_edges, color):

        #Set colors
        current_color = (color-1)%2
        for i in range(12):
            hexagon_half_edges[i].color = current_color
            current_color = (color-1)%2

        #Set opposite edges
        iter = 0
        while iter < 11:
            hexagon_half_edges[iter].opposite = hexagon_half_edges[iter+1]
            hexagon_half_edges[iter+1].opposite = hexagon_half_edges[iter]
            iter += 2

        #Set next and prior half-edges. Here prior and next are the same
        iter = 1
        while iter < 12:
            hexagon_half_edges[iter].next = hexagon_half_edges[iter+1]
            hexagon_half_edges[iter].prior = hexagon_half_edges[iter+1]
            hexagon_half_edges[iter+1].next = hexagon_half_edges[iter]
            hexagon_half_edges[iter+1].prior = hexagon_half_edges[iter]
            iter +=2
        #Return the starting half-edge
        return hexagon_half_edges[0]


    #Transforms a list of hexagon half-edges into a netowrkx graph
    def ___hexagon_to_graph(half_edges):

        ___construct_hexagon(half_edges)
        G = nx.Graph()
        list_size = len(half_edges)
        iter = 0
        count_unpaired = 0
        starting_half_edge = half_edges[0]

        current_half_edge = starting_half_edge
        while True:
            if current_half_edge == starting_half_edge:
                break 
                
            #Add new node with the color of the current half-edge
            G.add_node(iter, color=half_edges[iter].color)
            
            if current_half_edge.opposite != None:
                #Add new node with the color of the opposite half-edge
                G.add_node(iter+1, color=half_edges[(iter+1)%list_size].color)
                G.add_edge(iter,(iter+1)%list_size)
            else:
                #The current half-edge has no opponent so the "empty node" is created
                count_unpaired += 1
                G.add_node(count_unpaired, color='empty')
                G.add_edge(iter, count_unpaired)

            current_half_edge = current_half_edge.next


    def ___reject(init_half_edge):
        pass


    def ___quadrangulate(init_half_edge):
        pass

    def ___quadrangulation_to_3_map(init_half_edge):
        pass


    def closure(binary_tree):
        init_half_edge = ___btree_to_planar_map(binary_tree)
        init_half_edge = ___bicolored_complete_closure(init_half_edge)
        if ___reject(init_half_edge):
            return None
        init_half_edge = ___quadrangulate(init_half_edge)
        init_half_edge = ___quadrangulation_to_3_map(init_half_edge)
        return init_half_edge






    #Transforms a list of planar map half-edged into a networkx graph
    def ___half_edges_to_graph(init_half_edge):
        G = nx.Graph()
        node_list = ___assign_half_edges_to_nodes(init_half_edge, 0)


 



    #Returns a list of half-edges and its corresponding node number
    def ___assign_half_edges_to_nodes(half_edge, node_nr):
        half_edges = []
        half_edges.append((half_edge, node_nr))
        prior_half_edge = half_edge.prior 
        half_edges.append((prior_half_edge, node_nr))
        next_half_edge = half_edge.next
        half_edges.append((next_half_edge, node_nr))

        if half_edge.opposite == None:
            return half_edges
        else:
            if half_edge.opposite != None:
                half_edge.opposite.opposite = None
                half_edges.append(___assign_half_edges_to_nodes(half_edge.opposite, node_nr+1))
            elif half_edge.next.opposite != None:
                half_edge.next.opposite.opposite = None
                half_edges.append(___assign_half_edges_to_nodes(half_edge.next.opposite, node_nr+2))
            elif half_edge.prior.opposite != None:
                half_edge.prior.opposite.opposite = None
                half_edges.append(___assign_half_edges_to_nodes(half_edge.prior.opposite, node_nr+3))
            else:
                return

def ___test():
    h1 = HalfEdge()
    h2 = HalfEdge()
    h3 = HalfEdge()
    h4 = HalfEdge()
    h5 = HalfEdge()
    h6 = HalfEdge()
    h7 = HalfEdge()
    h8 = HalfEdge()
    h9 = HalfEdge()
    h10 = HalfEdge()
    h11 = HalfEdge()
    h12 = HalfEdge()
    h13 = HalfEdge()
    h14 = HalfEdge()
    h15 = HalfEdge()

    h1.opposite = None
    h1.next = h2 
    h1.prior = h3
    h2.opposite = h4
    h2.next = h3 
    h2.prior = h1
    h3.opposite = h7
    h3.next = h1
    h3.prior = h2
    h4.opposite = h2
    h4.next = h5
    h4.prior = h6
    h5.opposite = h10
    h5.next = h6
    h5.prior = h4
    h6.opposite = h13
    h6.next = h4
    h6.prior = h5
    h7.opposite = h3
    h7.next = h8
    h7.prior = h9
    h8.opposite = None
    h8.next = h9
    h8.prior = h7
    h9.opposite = None
    h9.next = h7
    h9.prior = h8
    h10.opposite = h5
    h10.next = h11
    h10.prior = h12
    h11.opposite = None
    h11.next = h12
    h11.prior = h10
    h12.opposite = None
    h12.next = h10
    h12.prior = h11
    h13.opposite = h6
    h13.next = h14
    h13.prior = h15
    h14.opposite = None
    h14.next = h15
    h14.prior = h13
    h15.opposite = None
    h15.next = h13
    h15.prior = h14

    half_edges = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15]

    print(___assign_half_edges_to_nodes(half_edges, 0))


            
            
            

        









