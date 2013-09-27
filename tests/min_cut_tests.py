'''
Created on Sep 5, 2013

@author: saxyseth
'''
import unittest

from min_cut.min_cut import AdjacencyList


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_AdjacencyList_update_vertex_list(self):
        adjacency_list = AdjacencyList(vertex_dict={1: [4, 3, 4], 2: [1, 3, 4], 3: [1, 4], 4: [1, 2, 5], 5: [4]},
                                    edge_list=[(1, 4), (1, 3), (2, 4), (2, 4), (1, 4), (4, 5)])
        edge_pair = (1, 4)
        new_vertex_name = 6
        adjacency_list.update_vertex_dict(edge_pair, new_vertex_name)
        print(adjacency_list.vertex_dict)
        print(adjacency_list.edge_list)
        self.assertNotIn(1, adjacency_list.vertex_dict)
        self.assertNotIn(4, adjacency_list.vertex_dict)

    def test_AdjacencyList_update_edg_list(self):
        adjacency_list = AdjacencyList(vertex_dict={1: [4, 3, 4], 2: [1, 3, 4], 3: [1, 4], 4: [1, 2, 5], 5: [4]},
                                    edge_list=[(1, 4), (1, 3), (2, 4), (2, 4), (1, 4), (4, 5)])
        edge_pair = (1, 4)
        new_vertex_name = 6
        adjacency_list.update_edge_list(edge_pair, new_vertex_name)
        print(adjacency_list.vertex_dict)
        print(adjacency_list.edge_list)
        self.assertNotIn((1, 4), adjacency_list.edge_list)
        self.assertIn((3, 6), adjacency_list.edge_list)
        self.assertIn((2, 6), adjacency_list.edge_list)
        self.assertIn((5, 6), adjacency_list.edge_list)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
