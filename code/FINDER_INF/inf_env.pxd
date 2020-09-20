from libcpp.vector cimport vector
from libcpp.set cimport set
from libcpp.memory cimport shared_ptr
from libcpp cimport bool
from igraph cimport Graph

cdef extern from "./src/lib/inf_env.h":
    cdef cppclass InfEnv:
        InfEnv(double _norm)
        void s0(shared_ptr[Graph] _g)except+
        double step(int a)except+
        void stepWithoutReward(int a)except+
        int randomAction()except+
        bool isTerminal()except+
        # double getReward(double oldCcNum)except+
        double getReward()except+
        double accurate_influence()except+
        double norm
        double inf_spread
        shared_ptr[Graph] graph
        vector[vector[int]]  state_seq
        vector[int] act_seq
        vector[int] action_list
        vector[double] reward_seq
        vector[double] sum_rewards
        vector[int] avail_list
