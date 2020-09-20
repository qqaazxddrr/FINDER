import numpy as np
import networkx as nx
import random
import copy
import time
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt


def set_py(input):
    return set(input)


def set_edge_weight(g):
    cur_n = len(g.nodes())
    a = nx.adjacency_matrix(g).todense()
    a = np.array(a + np.eye(cur_n))
    b = np.random.rand(cur_n, cur_n)
    c = a * b
    edge_weight = normalize(c, axis=0, norm='l1')
    return edge_weight


def preprocess(g):
    if type(g) == nx.MultiGraph or type(g) == nx.MultiDiGraph:
        raise Exception(
            "linear_threshold() is not defined for graphs with multiedges.")

    # change to directed graph
    if not g.is_directed():
        DG = g.to_directed()
    else:
        DG = copy.deepcopy(g)  # copy.deepcopy 深拷贝 拷贝对象及其子对象

    # init thresholds
    for n in DG.nodes():
        if 'threshold' not in DG.node[n]:
            DG.node[n]['threshold'] = random.random()
        elif DG.node[n]['threshold'] > 1:
            raise Exception("node threshold:", DG.node[n]['threshold'],
                            "cannot be larger than 1")

    edge_weight = set_edge_weight(DG)

    # init influence weight
    for e in DG.edges():
        if 'influence' not in DG[e[0]][e[1]]:
            DG[e[0]][e[1]]['influence'] = edge_weight[e[0]][e[1]]  # 设置边的权重
        elif DG[e[0]][e[1]]['influence'] > 1:
            raise Exception("edge influence:", DG[e[0]][e[1]]['influence'], \
                            "cannot be larger than 1")
    return DG


class inf_utils:
    def __init__(self, g, seeds):
        self.g = g
        self.seeds = seeds

    def _influence_sum(self, G, froms, to):
        influence_sum = 0.0
        for f in froms:
            influence_sum += G[f][to]['influence']
        return influence_sum

    def _diffuse_one_round(self, G, A):
        activated_nodes_of_this_round = set()
        for s in A:
            nbs = G.successors(s)
            for nb in nbs:
                if nb in A:
                    continue
                active_nb = list(set(G.predecessors(nb)).intersection(set(A)))
                if self._influence_sum(G, active_nb, nb) >= G.node[nb]['threshold']:
                    activated_nodes_of_this_round.add(nb)
        A.extend(list(activated_nodes_of_this_round))
        return A, list(activated_nodes_of_this_round)

    def _diffuse_all(self, g, A):
        layer_i_nodes = []
        layer_i_nodes.append([i for i in A])
        while True:
            len_old = len(A)
            A, activated_nodes_of_this_round = self._diffuse_one_round(g, A)
            layer_i_nodes.append(activated_nodes_of_this_round)
            if len(A) == len_old:
                break
        return layer_i_nodes

    def accurate_influence(self):
        # perform diffusion
        A = copy.deepcopy(self.seeds)
        result = self._diffuse_all(self.g, A)
        result_flat = [item for sublist in result for item in sublist]
        return len(result_flat), len(result_flat) / len(self.g.nodes())

    def live_edge(self, iter):
        covered_list = []
        for t in range(iter):
            # live-edge sample
            live_edge_sample = nx.DiGraph()
            for v in self.g.nodes():
                u_list = list(self.g.predecessors(v))
                weights = [self.g[u][v]['influence'] for u in u_list]
                u_list.append(v)
                weights.append(1 - sum(weights))
                u_select = np.random.choice(u_list, p=weights)
                if v != u_select:
                    live_edge_sample.add_edge(u_select, v)

            covered = set()
            for s in seed:
                if s in live_edge_sample.nodes():
                    _coverd_by_a_seed = set(nx.bfs_tree(live_edge_sample, s))
                    covered = covered.union(_coverd_by_a_seed, covered)
            covered_list.append(len(covered))
        coverd_mean = sum(covered_list) / len(covered_list)
        return coverd_mean, coverd_mean / len(self.g.nodes())


if __name__ == "__main__":
    max_n = 500
    min_n = 300
    seed_perc = 0.1
    le_iter = 10
    cur_n = np.random.randint(max_n - min_n + 1) + min_n
    g_synthesis = nx.barabasi_albert_graph(n=cur_n, m=4)
    DG, seeds = preprocess(g_synthesis)
    inf = inf_utils(DG, seeds)
    influence_auc, influence_auc_pct = inf.accurate_influence()
    print("{},{}".format(influence_auc, influence_auc_pct))
    influence_auc, influence_auc_pct = inf.accurate_influence()
    print("{},{}".format(influence_auc, influence_auc_pct))
