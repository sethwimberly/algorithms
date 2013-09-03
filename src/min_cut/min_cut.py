'''
Created on Sep 2, 2013

@author: swimberly
'''
import random


def read_file(filename):
    '''
    Read the file containing the adjacency list and convert the file into a list of vertices and a list of edges.
    edges represented as: (<vertex1_num, vertex2_num)
    vertices represented as: {vertex_num: [<adjacent_vertex>, <adjacent_vertex>}, ...}
    @return: A list of edges, and a list of vertices
    '''
    vertex_dict = {}
    edge_list = []
    with open(filename, 'r') as file:
        for row in file:
            row_list = row.split()
            vertex_num = row_list[0]
            adjacencies = row_list[1:]
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
    def __init__(self, filename):
        edge_list, vertex_dict = read_file(filename)
        self.edge_list = edge_list
        self.vertex_dict = vertex_dict

    def do_random_contraction(self):
        '''
        randomly select an edge and perform a contraction of the vertices contected by that edge
        '''
        if len(self.edge_list) == 0:
            print('bad')
        edge_pair = random.choice(self.edge_list)
        self.contract(edge_pair)

    def contract(self, edge_pair):
        '''
        given an edge, contract the two vertices connected by that edge.
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
                continue
            for old_vert in edge_pair:
                if old_vert in self.vertex_dict[vertex]:
                    #old_vert_index = self.vertex_dict[vertex].index(old_vert)
                    self.vertex_dict[vertex] = replace_all(self.vertex_dict[vertex], old_vert, new_vertex_name)
                    #self.vertex_dict[vertex][old_vert_index] = new_vertex_name

        #print(edge_pair)
        #print(self.vertex_dict)
        #print(self.edge_list)
        #print()
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

        #print('after')
        #print(self.vertex_dict)
        #print(self.edge_list)
        #print()

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
            if edge_pair[0] in pair:
                new_pair = (new_vertex_name, new_pair[1])
            if edge_pair[1] in pair:
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
    '''
    min_cuts = []
    adjacent_list = AdjacencyList(filename)
    for _i in range(attempt_num):
        min_cut = single_run_random_min_cut(adjacent_list)
        min_cuts.append(min_cut)

    return min(min_cuts)


def single_run_random_min_cut(adjacent_list):
    '''
    '''
    while len(adjacent_list.vertex_dict) > 2:
        adjacent_list.do_random_contraction()

    min_cuts = []
    for vert in adjacent_list.vertex_dict:
        min_cut = len(adjacent_list.vertex_dict[vert])
        print(vert, adjacent_list.vertex_dict[vert])
        min_cuts.append(min_cut)
    print('min_cuts', min_cuts[0], min_cuts[1])
    print(adjacent_list.edge_list)
    print(adjacent_list.vertex_dict)
    #assert min_cuts[0] == min_cuts[1]
    return min_cuts[0]

if __name__ == '__main__':
    #result = read_file('/Users/swimberly/Documents/sethwimberly-git/algorithms/test_files/min_cut/kargerMinCut.txt')
    adj_list = AdjacencyList('/Users/swimberly/Documents/sethwimberly-git/algorithms/test_files/min_cut/kargerMinCut.txt')
    adj_list.edge_list = [(1, 2), (1, 3), (1, 4), (2, 1), (2, 3), (2, 4), (4, 1), (4, 2), (4, 5), (5, 4)]
    adj_list.vertex_dict = {1: [2, 3, 4], 2: [1, 3, 4], 3: [1, 2], 4: [1, 2, 5], 5: [4]}
    #adj_list.contract((1, 3))
#    print(adj_list.vertex_dict)
#    print(adj_list.edge_list)

    print()

    single_run_random_min_cut(adj_list)
    #print(multi_run_random_min_cut('/Users/swimberly/Documents/sethwimberly-git/algorithms/test_files/min_cut/kargerMinCut.txt'))
