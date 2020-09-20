from cython.operator import dereference as deref
from libcpp.memory cimport shared_ptr
import numpy as np
import igraph
from igraph cimport Graph
import inf_utils
import copy
import gc
from libc.stdlib cimport free

cdef class py_InfEnv:
    cdef shared_ptr[InfEnv] inner_InfEnv
    cdef shared_ptr[Graph] inner_Graph
    cdef double inf_spread

    def __cinit__(self, double _norm):
        self.inner_InfEnv = shared_ptr[InfEnv](new InfEnv(_norm))
        self.inner_Graph = shared_ptr[Graph](new Graph())
        self.inf_spread = 0.0

    # def __dealloc__(self):
    #     if self.inner_MvcEnv != NULL:
    #         self.inner_MvcEnv.reset()
    #         gc.collect()
    #     if self.inner_Graph != NULL:
    #         self.inner_Graph.reset()
    #         gc.collect()
    def s0(self, _g_inner):
        self.inner_Graph = shared_ptr[Graph](new Graph())
        deref(self.inner_Graph).num_nodes = _g_inner.num_nodes
        deref(self.inner_Graph).num_edges = _g_inner.num_edges
        deref(self.inner_Graph).edge_list = _g_inner.edge_list
        deref(self.inner_Graph).adj_list = _g_inner.adj_list
        deref(self.inner_InfEnv).s0(self.inner_Graph)

    def step(self, int a):
        return deref(self.inner_InfEnv).step(a)

    def stepWithoutReward(self, int a):
        deref(self.inner_InfEnv).stepWithoutReward(a)

    def randomAction(self):
        return deref(self.inner_InfEnv).randomAction()

    def isTerminal(self):
        return deref(self.inner_InfEnv).isTerminal()

    def getReward(self):
        return deref(self.inner_InfEnv).getReward()

    def accurate_influence(self):
        return deref(self.inner_InfEnv).accurate_influence()

    @property
    def norm(self):
        return deref(self.inner_InfEnv).norm

    @property
    def graph(self):
        # temp_innerGraph=deref(self.inner_Graph)   #得到了Graph 对象
        return self.G2P(deref(self.inner_Graph))

    @property
    def state_seq(self):
        return deref(self.inner_InfEnv).state_seq

    @property
    def act_seq(self):
        return deref(self.inner_InfEnv).act_seq

    @property
    def action_list(self):
        return deref(self.inner_InfEnv).action_list

    @property
    def reward_seq(self):
        return deref(self.inner_InfEnv).reward_seq

    @property
    def sum_rewards(self):
        return deref(self.inner_InfEnv).sum_rewards

    @property
    def inf_spread(self):
        return deref(self.inner_InfEnv).inf_spread

    @property
    def avail_list(self):
        return deref(self.inner_InfEnv).avail_list

    cdef G2P(self, Graph graph1):
        num_nodes = graph1.num_nodes  #得到Graph对象的节点个数
        num_edges = graph1.num_edges  #得到Graph对象的连边个数
        edge_list = graph1.edge_list
        cint_edges_from = np.zeros([num_edges], dtype=np.int)
        cint_edges_to = np.zeros([num_edges], dtype=np.int)
        for i in range(num_edges):
            cint_edges_from[i] = edge_list[i].first
            cint_edges_to[i] = edge_list[i].second
        return igraph.py_Graph(num_nodes, num_edges, cint_edges_from, cint_edges_to)
