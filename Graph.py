import itertools
import networkx as nx
import GenericFunctions as gf

# This function creates a graph's nodes without edges
def create_graph(inf_data):   
    graph=nx.Graph()
    dict_aut={} 
# These 2 'for' loops create nodes and their corresponding attributes
    for i in range(len(inf_data)):
        for auth in inf_data[i]["authors"]:
            try:
                auth["author_id"]
                dict_aut[auth["author_id"]]["id_publication_int"].add(inf_data[i]["id_publication_int"])
                dict_aut[auth["author_id"]]["id_conference_int"].add(inf_data[i]["id_conference_int"])
            except:
                dict_aut[auth["author_id"]]={}
                dict_aut[auth["author_id"]]["id_publication_int"]=set()
                dict_aut[auth["author_id"]]["id_conference_int"]=set()
                dict_aut[auth["author_id"]]["id_publication_int"].add(inf_data[i]["id_publication_int"])
                dict_aut[auth["author_id"]]["id_conference_int"].add(inf_data[i]["id_conference_int"])
                
            graph.add_node(auth["author_id"], name_author=gf.clean_name(auth["author"]), id_publication_int=list(dict_aut[auth["author_id"]]['id_publication_int']),
                          id_conference_int=list(dict_aut[auth["author_id"]]['id_conference_int']))
    return graph

# This function creates weighted graph's edges
def add_edges(inf_data,graph):
    list_id_name=[[id_name['author_id'] for id_name in elem['authors']] for elem in inf_data if len(elem['authors'])>1]
    # This 'for' loop creates the edges of the graph, taking them from a set of tuples, where there are all possible 
    # combinations between nodes which are connected
    for edge in {subset for elem in list_id_name for subset in itertools.combinations(elem,2)}:
        graph.add_edge(edge[0],edge[1],weight=1-gf.jaccard_similarity(graph.node[edge[0]]['id_publication_int'],graph.node[edge[1]]['id_publication_int']))



