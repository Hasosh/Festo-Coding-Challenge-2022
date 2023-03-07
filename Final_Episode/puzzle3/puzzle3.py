import pickle
import pprint
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt


class Graph_normal(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.items():  # python3: items(); python2: iteritems()
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

def test():	
	pass

def main(file):
    edges, edges_and_weights = process_machine_room(file)

    # create normal graph
    # g = Graph_normal(edges)
    # pretty_print = pprint.PrettyPrinter()
    # pretty_print.pprint(g._graph)
    # print(g.find_path('A','Z'))

    #visualize_graph(edges, edges_and_weights)

    #https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.minimum_cut.html
    G = nx.Graph()
    for e in edges_and_weights:
        G.add_edge(e[0], e[1], capacity=e[2])

    cut_value, partition = nx.minimum_cut(G, "A", "Z")
    reachable, non_reachable = partition
    print("Minimum Cut Value: ", cut_value)
    print("Partition of Nodes: ", reachable, non_reachable)

    cutset = set()
    for u, nbrs in ((n, G[n]) for n in reachable):
        cutset.update((u, v) for v in nbrs if v in non_reachable)
    print("Cutset of edges: ", sorted(cutset))
    cut_value == sum(G.edges[u, v]["capacity"] for (u, v) in cutset)
    save_list(sorted(cutset))

def process_machine_room(file):
    with open(file, "r") as filestream:
        edges = []
        edges_and_weights = []
        for l in filestream:
            splitted = [a.strip() for a in l.split(":")]
            edge = (splitted[1][0], splitted[1][-1])
            weight = int(splitted[2])
            edges.append(edge)
            edges_and_weights.append(edge + (weight,))
        return edges, edges_and_weights

def visualize_graph(edges, edges_and_weights):
    # ALTERNATIVE
    # G = nx.Graph()
    # G.add_edges_from(edges)
    # pos=nx.spring_layout(G) # pos = nx.nx_agraph.graphviz_layout(G)
    # nx.draw_networkx(G,pos)
    # labels = nx.get_edge_attributes(G,'weight')
    # nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

    #create graph 2 for visualizing
    G = nx.Graph()
    for e in edges_and_weights:
        G.add_edge(e[0], e[1], weight=e[2])
    
    #https://networkx.org/documentation/stable/auto_examples/drawing/plot_weighted_graph.html

    #elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 10]
    #esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 10]

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=6)

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    plt.show()

def save_list(mylist):
    with open('solution_sequence.pkl', 'wb') as f:
        pickle.dump(mylist, f)

if __name__ == '__main__':
	machine_room_file = "machine_room.txt"
	#test()
	main(machine_room_file)