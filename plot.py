import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy
import Hopdistance as hd
import GenericFunctions as gf

# This function plots the subgraph of the nodes (authors) participating in the same conference.
def create_graph_by_conf(G_def, conf):
    
# Divide all nodes in 4 groups by the number of edges for each node
    node_2_conn=[node for node in G_def.nodes() if len(G_def[node]) <=2 ] 
    node_2_6_conn=[node for node in G_def.nodes() if len(G_def[node])>2 and len(G_def[node])<=6  ]
    node_6_10_conn=[node for node in G_def.nodes() if len(G_def[node])>6 and len(G_def[node])<=10 ]
    node_10_15_conn=[node for node in G_def.nodes() if len(G_def[node])>10]
              
    node_size=[]
    for node in G_def.nodes():
        if node in node_2_conn:
            node_size.append(5)
        elif node in node_2_6_conn:
            node_size.append(10)
        elif node in node_6_10_conn:
            node_size.append(80)
        elif node in node_10_15_conn:
            node_size.append(100)
        else:
            node_size.append(200)
# Give a colour to more important nodes (which have a lot of connections)        
    node_colours=[]
    for node in G_def.nodes():
        if node in node_10_15_conn:
            node_colours.append('lightcoral')
        else:
            node_colours.append('dodgerblue')
# Plot subgraph
    fig = plt.figure()
    nx.draw(G_def,pos=nx.spring_layout(G_def), 
            cmap=plt.get_cmap('jet'),
            node_color =node_colours,
            node_size = node_size,
            width=0.5,
            style='dotted',
            alpha=0.9)
    fig.suptitle('Graph of the conference: ' + str(conf), fontsize=14, fontweight='bold', color='firebrick')

    lightcoral_patch = mpatches.Patch(color='lightcoral', label='degree > 10')
    
    plt.legend(handles=[lightcoral_patch], loc=1)
    plt.savefig('create_graph_by_conf.png')

    plt.show()
    plt.close()


# This function creates a histogram that rapresnt illustrating betweenness, degree and closeness centalities
def statistics_by_conf(G_sub, conf):
    # Degree centrality
    Deg_centrality=nx.degree_centrality(G_sub)
    # Closeness centrality
    Clos_centrality=nx.closeness_centrality(G_sub)
    # Betweenness centrality
    Betw_centrality=nx.betweenness_centrality(G_sub)
    
    plt.figure()
    bins = numpy.linspace(0, 0.040, 40)
# Plot histogram
    plt.hist(list(Deg_centrality.values()), bins,normed=True, facecolor='gold', alpha=0.50)
    plt.hist(list(Clos_centrality.values()),bins, normed=True, facecolor='orchid', alpha=0.50)
    plt.hist(list(Betw_centrality.values()), bins, normed=True,  facecolor='turquoise', alpha=0.50)
    plt.xlabel('Centrality')
    plt.ylabel('Frequency')
    plt.title('Statistics of the conference graph: ' + str(conf))
    gold_patch = mpatches.Patch(color='gold', label='Degree centrality',alpha=0.50)
    orchid_patch = mpatches.Patch(color='orchid', label='Closness centrality',alpha=0.50)
    turquoise_patch = mpatches.Patch(color='turquoise', label='Betweenness centrality',alpha=0.50)
    
    plt.legend(handles=[gold_patch,orchid_patch,turquoise_patch ], loc=1)
    plt.savefig('statistics_by_conf.png')

    plt.show()
    plt.close()

    
# This funcion creates a plot showing the main node (i.e. the input author), and 
# the adjacent nodes (with hop distance equal to the input d previously mentioned)
def create_graph_by_auth(node,G_def):
    starter=node
    Hd=hd.Hop_Dist(G_def)
# Divide all nodes in 4 groups by the hop distance level of the input node
    first_node=Hd.hop_distance(1, node)
    second_level_node=[i for i in Hd.hop_distance(2, node) if i not in Hd.hop_distance(1, node)]
    third_level_node=[i for i in Hd.hop_distance(3, node) if i not in Hd.hop_distance(2, node)]
    
    node_colours=[]
    for node in G_def.nodes():
        if node in first_node:
            node_colours.append('red')
        elif node in second_level_node:
            node_colours.append('lightcoral')
        elif node in third_level_node:
            node_colours.append('orchid')
        else:
            node_colours.append('dodgerblue')
                
    node_2_conn=[node for node in G_def.nodes() if len(G_def[node]) <=2 ] 
    node_2_6_conn=[node for node in G_def.nodes() if len(G_def[node])>2 and len(G_def[node])<=6  ]
    node_6_10_conn=[node for node in G_def.nodes() if len(G_def[node])>6 and len(G_def[node])<=10 ]
    node_10_15_conn=[node for node in G_def.nodes() if len(G_def[node])>10 and len(G_def[node])<=15 ]
                
    node_size=[]
    for node in G_def.nodes():
        if node in node_2_conn:
            node_size.append(5)
        elif node in node_2_6_conn:
            node_size.append(10)
        elif node in node_6_10_conn:
            node_size.append(80)
        elif node in node_10_15_conn:
            node_size.append(100)
        else:
            node_size.append(200)
            
# Plot subgraph    
    fig = plt.figure()
    nx.draw(G_def,pos=nx.spring_layout(G_def), 
            cmap=plt.get_cmap('jet'),
            node_color =node_colours,
            node_size = node_size,
            width=0.5,
            style='dotted',
            alpha=0.9)
    fig.suptitle('Subgraph of level of hop distance from %s. ' %(starter), fontsize=14, fontweight='bold', color='firebrick')
    red_patch = mpatches.Patch(color='red', label='d=1')
    lightcoral_patch = mpatches.Patch(color='lightcoral', label='d=2')
    orchid_patch = mpatches.Patch(color='orchid', label='d=3')
    dodgerblue_patch = mpatches.Patch(color='dodgerblue', label='d>3')
    

    plt.legend(handles=[red_patch, lightcoral_patch, orchid_patch, dodgerblue_patch], loc=1)

    plt.savefig('create_graph_by_auth.png')

    plt.show()
    plt.close()


# This function creates a plot of the shortest path between any two nodes. 
def create_plot_shorter_path(G,tup_node):
    G_dij=G.subgraph(tup_node[1])
    weight=round(float(tup_node[0]),3)
# Plot the shortest path
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    pos = nx.spring_layout(G_dij)
    nx.draw_networkx_nodes(G_dij, pos, cmap=plt.get_cmap('jet'), 
                           node_color = 'dodgerblue', node_size = 500, alpha=0.6)
    label={node:gf.Id_name(G_dij,node) for node in G_dij.nodes()}
    nx.draw_networkx_labels(G_dij,pos,label,font_size=8)
    nx.draw_networkx_edges(G_dij, pos, edge_color='r', style='dotted' ,arrows=True)
    fig.suptitle('The Shortest Path between : ' + str(gf.Id_name(G_dij,tup_node[1][0]))
    + ' and ' +str(gf.Id_name(G_dij,tup_node[1][-1])), fontsize=14, fontweight='bold', color='firebrick')
    
    ax.set_title( 'Cost = ' + str(weight), color='red')
    plt.savefig('create_plot_shorter_path.png')

    plt.show()
    plt.close()
    
