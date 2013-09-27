'''
Created on Sep 7, 2013

@author: swimberly

compute strongly connected components of a graph using Kosaraju's algorithm

TODO: Use iterative DFS instead of recursive version for speed
TODO: Use a more memory efficient method for maintaining nodes
'''
import argparse
import sys
import threading
threading.stack_size(2 ** 27)
sys.setrecursionlimit(2 ** 25)

# Global Variables
number_nodes_so_far = None
source_vertex = None


def compute_scc(graph, graph_rev):
    '''
    Compute the strongly connected components of a graph
    @param graph: the Graph object
    @param graph_rev: the Graph object representing the reverse of the graph
    @return: A list of nodes by their respective leaders
    '''
    print('Starting pass 1')
    dfs_loop(graph_rev, 1)
    graph.node_map = graph_rev.nodes_by_finishing_time
    print('Starting pass 2')
    dfs_loop(graph, 2)

    scc = graph.nodes_by_leader
    return scc


def dfs_loop(graph, pass_num):
    '''
    Loop through the vertices of the graph and do a depth first search on each
    @param graph: The graph object to perform the depth first search on
    @param pass_num: pass 1 or pass 2
    '''
    global number_nodes_so_far
    number_nodes_so_far = 0
    global source_vertex
    source_vertex = 0

    for i in range(len(graph.vertex_dict), 0, -1):
        node = i if pass_num == 1 else graph.node_map[i]

        if node not in graph.explored:
            source_vertex = node
            dfs(graph, node)


def dfs(graph, start_node):
    '''
    Perform a depth first search on each node starting at the start node
    @param graph: graph object to search
    @param start_node: where to initiate the search
    '''
    # use global copy of number_nodes_so_far
    global number_nodes_so_far

    # update the explored set with the new node
    explored = graph.explored
    explored.add(start_node)

    # update leaders list
    graph.nodes_by_leader[source_vertex] = graph.nodes_by_leader.get(source_vertex, []) + [start_node]

    # loop edges from the start_node and dfs on each
    for vertex in graph.vertex_dict[start_node]:
        if vertex not in explored:
            dfs(graph, vertex)

    # update the number of nodes seen so far
    number_nodes_so_far += 1

    # update the finishing time
    graph.nodes_by_finishing_time[number_nodes_so_far] = start_node


def read_file(filename):
    '''
    Read the file and create 2 graphs G and Grev
    @param filename: the name of the file to read
    @return: the graph object and a graph object containing its revers
    '''
    print('Reading file')

    vertex_dict = {}
    vertex_dict_rev = {}
    with open(filename, 'r') as file:
        for row in file:
            # create edge pair
            pair = tuple([int(x) for x in row.split()])

            # update vertex lists, ensure all vertices have values in the dict
            vertex_dict[pair[0]] = vertex_dict.get(pair[0], []) + [pair[1]]
            vertex_dict[pair[1]] = vertex_dict.get(pair[1], [])

            vertex_dict_rev[pair[1]] = vertex_dict_rev.get(pair[1], []) + [pair[0]]
            vertex_dict_rev[pair[0]] = vertex_dict_rev.get(pair[0], [])

    graph = Graph(vertex_dict)
    graph_rev = Graph(vertex_dict_rev)

    return graph, graph_rev


def find_max_scc(strongly_connecteds, num_counts):
    '''
    Given a list of sccs, sort and return the first <num_counts> values
    @param strongly_connecteds: a dict representing each leader and their list of
    connected vertices
    @param num_counts: the maximum number of values to return
    @return: A list of highest counts of sccs
    '''
    print('finding max')
    scc_counts = [len(scc_list) for _scc, scc_list in strongly_connecteds.items()]
    return sorted(scc_counts, reverse=True)[:num_counts]


class Graph(object):
    '''
    Object for representing a graph
    '''
    def __init__(self, vertex_dict):
        ''' Constructor '''
        self.vertex_dict = vertex_dict

        self.explored = set()
        self.nodes_by_finishing_time = {}
        self.nodes_by_leader = {}
        self.node_map = {}


def main(filename):
    g, gr = read_file(filename)

    scc = compute_scc(g, gr)

    print(find_max_scc(scc, 5))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Strongly Connected Components')
    parser.add_argument('-f', '--filename', required=True, help='The name of the file')

    args = parser.parse_args()
    #main(args.filename)

    thread = threading.Thread(target=main, args=[args.filename])
    thread.start()
