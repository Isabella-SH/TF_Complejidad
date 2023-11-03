import graphviz as gv
import networkx as nx
import matplotlib.pyplot as plt


class Graph:

    def __init__(self):
        self.Nodes = []  # Lista de objetos House
        self.G = []

    def add_node(self, node):
        self.Nodes.append(node)
        self.G.append([])

    def add_edge(self, u, v):
        u_id = self.Nodes.index(u)
        v_id = self.Nodes.index(v)
        self.G[u_id].append((v_id, 10))


    def add_weighted_edge(self, u, v, weight):
        u_id = self.Nodes.index(u)
        v_id = self.Nodes.index(v)
        #print(f"u_id: {u_id}, v_id: {v_id}")
        #print(f"Peso:{weight}")
        #print("\n")
        self.G[u_id].append((v_id, weight))
        

    def get_node_label(self, u):
        return self.Nodes[u]

    def get_edges(self, u):
        return self.G[u]
    
    def obtener_nodos(self):
        return self.Nodes

    def num_nodes(self):
        return len(self.Vertices)

    def Dot(self):
        graph = gv.Digraph("X")
        n = len(self.G)
        for u in range(n):
            graph.node(str(u), str(self.Vertices[u].ID()))

        for u in range(n):
            for v, w in self.G[u]:
                graph.edge(str(u), str(v), str(w))
        return graph
    
'''
def drawG_al(G, weighted=False, directed=False):
    nxG = nx.Graph() if not directed else nx.DiGraph()

    for casa in G.Nodes:
        nxG.add_node(casa)

    for u in range(len(G.G)):
        for v, w in G.G[u]:
            nxG.add_edge(G.get_node_label(u), G.get_node_label(v), weight=w if weighted else 1)

    pos = nx.spring_layout(nxG)  # Puedes elegir otro layout si prefieres

    if weighted:
        edge_labels = {(u, v): d['weight'] for u, v, d in nxG.edges(data=True)}
        nx.draw_networkx_edge_labels(nxG, pos, edge_labels=edge_labels)

    nx.draw(nxG, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_color='black')

    plt.show()
    '''
    
def drawG_al(G, weighted=False, directed=False):
    nxG = nx.Graph() if not directed else nx.DiGraph()

    for u in range(len(G.Nodes)):  # Agregar nodos con sus índices como etiquetas
        nxG.add_node(u)

    for u in range(len(G.G)):
        for v, w in G.G[u]:
            nxG.add_edge(u, v, weight=w if weighted else 1)

    pos = nx.spring_layout(nxG)  # Puedes elegir otro layout si prefieres

    if weighted:
        edge_labels = {(u, v): d['weight'] for u, v, d in nxG.edges(data=True)}
        nx.draw_networkx_edge_labels(nxG, pos, edge_labels=edge_labels)

    nx.draw(nxG, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_color='black', labels={node: node for node in nxG.nodes()})

    plt.show()



def drawG_al_2(G, directed=False, weighted=False, path=[], layout="sfdp"):
    graph = gv.Digraph("digrafo") if directed else gv.Graph("grafo")
    graph.graph_attr["layout"] = layout
    graph.edge_attr["color"] = "gray"
    graph.node_attr["color"] = "orangered"
    graph.node_attr["width"] = "0.1"
    graph.node_attr["height"] = "0.1"
    graph.node_attr["fontsize"] = "8"
    graph.node_attr["fontcolor"] = "mediumslateblue"
    graph.node_attr["fontname"] = "monospace"
    graph.edge_attr["fontsize"] = "8"
    graph.edge_attr["fontname"] = "monospace"

    n = len(G.G)  # Utilizamos la longitud de G

    added = set()

    for v, u in enumerate(path):
        if u != -1:
            if weighted:
                for vi, w in G.G[u]:
                    if vi == v:
                        print(f"Peso arista {u}-{v}: {w}")  # Agrega esta línea para verificar el peso
                        break

                graph.edge(str(u), str(v), label=str(w), dir="forward", penwidth="2", color="orange")
                        
            else:
                graph.edge(str(u), str(v), dir="forward", penwidth="2", color="orange")
            added.add(f"{u},{v}")
            added.add(f"{v},{u}")

    for u in range(n):
        for v, w in G.G[u]:
            draw = False
            if not directed and not f"{u},{v}" in added:
                added.add(f"{u},{v}")
                added.add(f"{v},{u}")
                draw = True
            elif directed:
                draw = True
            if draw:
                if weighted:
                    graph.edge(str(u), str(v), label=str(w))
                else:
                    graph.edge(str(u), str(v))

    return graph
