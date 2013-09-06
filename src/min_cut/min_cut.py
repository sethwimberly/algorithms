'''
Created on Sep 2, 2013

@author: swimberly
'''

import random
import argparse


def read_file(filename):
    '''
    Read the file containing the adjacency list and convert the file into a list of vertices and a list of edges.
    edges represented as: (<vertex1_num, vertex2_num)
    vertices represented as: {vertex_num: [<adjacent_vertex>, <adjacent_vertex>}, ...}
    Assumes that all vertices are integers
    @return: A list of edges, and a list of vertices
    '''
    vertex_dict = {}
    edge_list = []
    with open(filename, 'r') as file:
        for row in file:
            row_list = row.split()
            vertex_num = int(row_list[0])
            adjacencies = [int(x) for x in row_list[1:]]
            vertex_dict[vertex_num] = adjacencies
            edges = [tuple(sorted([vertex_num, vertex2])) for vertex2 in adjacencies]
            edge_list += edges

    # remove duplicates from edge_list
    edge_list = list(set(edge_list))
    return edge_list, vertex_dict


def replace_all(vertex_list, old_val, new_val):
    '''
    Take a list of vertices and replace all occurences of the old value with the new value
    '''
    return [x if x != old_val else new_val for x in vertex_list]


class AdjacencyList(object):
    '''
    Object for maintaining the components of the adjacency list
    '''
    def __init__(self, filename=None, edge_list=None, vertex_dict=None):
        if filename:
            edge_list, vertex_dict = read_file(filename)
        self.edge_list = edge_list
        self.vertex_dict = vertex_dict

    def do_random_contraction(self):
        '''
        randomly select an edge and perform a contraction of the vertices contected by that edge
        '''
        edge_pair = random.choice(self.edge_list)
        self.contract(edge_pair)

    def contract(self, edge_pair):
        '''
        given an edge, contract the two vertices connected by that edge.
        @param edge_pair: A pair of vertices. ie. (2, 5)
        '''
        new_vertex_name = edge_pair[0]
        self.update_edge_list(edge_pair, new_vertex_name)
        self.update_vertex_dict(edge_pair, new_vertex_name)

    def update_vertex_dict(self, edge_pair, new_vertex_name):
        '''
        Loop trough the vertices and update their connection lists wit the new name of the vertex.
        Combine the list for the two vertices in the edge_pair
        '''
        # Convert all occurrences of the edge_pair values to the new_vertex name
        for vertex in self.vertex_dict:
            if vertex in edge_pair:
                # Skip this case as it is removed later
                continue

            for old_vert in edge_pair:
                # replace all occurences of the old vertex name with the new name
                self.vertex_dict[vertex] = replace_all(self.vertex_dict[vertex], old_vert, new_vertex_name)

        # pull out the values in each of the lists
        vert1_list = self.vertex_dict[edge_pair[0]]
        vert2_list = self.vertex_dict[edge_pair[1]]
        # Create a new list that combines the two lists and removes occurrences of the new vertex_name
        new_vert_list = list(filter(lambda a: a not in [new_vertex_name] + list(edge_pair), vert1_list + vert2_list))

        # Delete the two items from the dict
        del self.vertex_dict[edge_pair[0]]
        del self.vertex_dict[edge_pair[1]]

        # add the new value
        self.vertex_dict[new_vertex_name] = new_vert_list

    def update_edge_list(self, edge_pair, new_vertex_name):
        '''
        Loop through the list of edge_pairs and make the following updates:
        for each pair that has one of the the mentioned vertices change that vertex to have the new name
        add the pairs to the new list only if tey aren't self loops
        '''
        new_edge_list = []
        for pair in self.edge_list:
            new_pair = pair

            # check if either vertex is in the pair
            if new_pair[0] in edge_pair:
                new_pair = (new_vertex_name, new_pair[1])
            if new_pair[1] in edge_pair:
                new_pair = (new_pair[0], new_vertex_name)

            # Order vertices in order to compare
            new_pair = tuple(sorted(new_pair))
            # Skip self loops
            if new_pair[0] != new_pair[1] and edge_pair != new_pair:
                new_edge_list.append(new_pair)
        # replace with new list
        self.edge_list = new_edge_list


def multi_run_random_min_cut(filename, attempt_num=10):
    '''
    Run the min cut multiple times and return the min result
    @param filename: The name of the file
    @param attempt_num: The number of attempts to make
    @return: the min of the minimum cut
    '''
    min_cuts = []
    for i in range(attempt_num):
        adjacent_list = AdjacencyList(filename)
        min_cut = single_run_random_min_cut(adjacent_list)
        min_cuts.append(min_cut)
        print('min cut from round %d: %d' % (i, min_cut))

    return min(min_cuts)


def single_run_random_min_cut(adjacent_list):
    '''
    Run the min cut once and return the result
    @param adjacent_list: An AdjacentList object
    @return: The min cut
    '''
    while len(adjacent_list.vertex_dict) > 2:
        adjacent_list.do_random_contraction()

    min_cuts = []
    for vert in adjacent_list.vertex_dict:
        min_cut = len(adjacent_list.vertex_dict[vert])
        min_cuts.append(min_cut)

    assert min_cuts[0] == min_cuts[1]
    return min_cuts[0]


def main(filename, rounds=10):
    '''
    main method
    @param filename: the name of the file
    '''
    print('Calculating min cut. Running %d rounds' % rounds)
    min_cut = multi_run_random_min_cut(filename, rounds)
    print('Final min cut:', min_cut)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Minimum Cut')
    parser.add_argument('-f', '--filename', required=True, help='Name of the file')
    parser.add_argument('-r', '--rounds', default=10, type=int,
                        help='The number of rounds to run the random min_cut. Default:10')
    args = parser.parse_args()

    main(args.filename, args.rounds)
