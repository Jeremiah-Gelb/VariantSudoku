import math
from . import solver

def test_reduce_value_options_based_on_neighbors():
   nodes = gen_node_neighbors(3)
   nodes[1].value_options = {1}
   nodes[2].value_options = {2}
   nodes[0].reduce_value_options_based_on_neighbors()
   
   assert nodes[0].value_options == {3, 4, 5, 6, 7, 8, 9}

def test_iteravely_reduce_value_options():
   nodes = gen_node_neighbors(6)
   nodes[0].value_options = {1, 2}
   nodes[1].value_options = {2, 3}
   nodes[2].value_options = {3, 4}
   nodes[3].value_options = {4, 5}
   nodes[4].value_options = {5, 6}
   nodes[5].value_options = {6}

   solver.iteravely_reduce_value_options(nodes)

   assert nodes[0].value_options == {1}
   assert nodes[1].value_options == {2}
   assert nodes[2].value_options == {3}
   assert nodes[3].value_options == {4}
   assert nodes[4].value_options == {5}
   assert nodes[5].value_options == {6}



def gen_node_neighbors(size) -> list[solver.Node]:
   nodes: list[solver.Node] = []
   for i in range(size):
      nodes.append(solver.Node())
      for j in range(i):
         nodes[j].add_neighbor(nodes[i])
         nodes[i].add_neighbor(nodes[j])
   return nodes
