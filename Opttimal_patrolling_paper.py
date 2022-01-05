import networkx as nx
import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt
import sys

'''add average idealness and max idealness and print walk.'''

#Graph_path= input("please provide the path to GraphML file ")
Graph_path = sys.argv[1]
#no_off_agents= int(input("Please provide number of agents no "))
no_off_agents = int(sys.argv[2])
GraphML= nx.read_graphml(Graph_path)          #Reading the GraphML file from the given input path

def DFSUtil(Graph, v, visited):
    '''The helper Recursive Function for DFS traversel'''
        # Mark the current node as visited and print it
    visited.append(v)
    #print(v)
 
        # recur for all the vertices adjacent to this vertex
    for neighbour in Graph.neighbors(v):
        if neighbour not in visited:
            DFSUtil(Graph,neighbour, visited)
    return visited


def DFS (Graph):
    '''This function takes a graph as input and return its Depth First Search
    # It uses recursive DFSUtil'''
    # create a list to store all visited vertices
    visited = list()
        # call the recursive helper function to print DFS traversal starting from all
        # vertices one by one
    for vertex in Graph.nodes:
        if vertex not in visited:
            DFSUtil(Graph,vertex, visited)
    return visited

def partition(G,l):
  Weight = "lenght"
  a=0
  pi=[]
  #print("l= ",l)
  while a<wg[-1]:
    #p = [(u,v) for (u,v,d) in G.edges(data=True) if d[Weight] <=(a+l) and d[Weight] >=a]
    p = [(u) for (u,d) in G.nodes(data=True) if d[Weight] <=(a+l) and d[Weight] >=a]
    pi.append(p)
    #print(pi)
    #a =[(u,v) for (u,v,d) in G.edges(data=True) if d[Weight]>=(a+l)]
    a = [(u) for (u,d) in G.nodes(data = True) if d[Weight] >= (a+l)]
    c = []
    for u in a:
      c.append(G.nodes[u][Weight])
    #print("c=",c)
    if len(c)==0:
      return pi
    else:
      a=min(c)
      #print("a=",a)
  return pi

#Graph=nx.Graph()
#elist = [(1,2, 1), (2,3, 2), (3,4, 4), (4,5, 5),(5,6,7),(6,7, 8),(7,8, 10),(8,9, 13),(9,10, 14)]
#Graph.add_weighted_edges_from(elist)
G=DFS(GraphML) 
wg=[]
for i in range(len(G)):
  cur=G[0]
  #dist=nx.dijkstra_path_length(GraphML, cur, G[i], weight = 'length')   #Dijkstra path lenght funtion
  dist = (i)*100  #lenght of each edge is 100 which is added in chain graph.
  wg.append(dist)
#G=range(len(G))
G=list(map(int,G))
wg=list(map(int,wg))
elist=[]
for i in range(len(G)-1):
  #elist.append((G[i],G[i+1],wg[i+1]))
  elist.append((G[i],G[i+1]))
#print("edgelist= ",elist)
Graph=nx.Graph()
#Graph.add_weighted_edges_from(elist)
Graph.add_edges_from(elist)
j=0
for i in Graph.nodes():
  Graph.nodes[i]["lenght"]=100*j
  j+=1
#print(Graph.edges(data=True))
#print(Graph.nodes(data=True))

'''setting the parameters for partitioning'''
a=0
delta=100
epsilon=0.01
m=no_off_agents
weight="lenght"
b=(wg[-1]+delta)/m
l=(a+b)/2
while (b-a)>2*epsilon:
  pi = partition(Graph,l)
  if pi==None:
    print("No partiontions available at current setting. Please use different Parameters")
    break
  if len(pi)>m:
    a=l
    l = (a + b)/2
#    print(pi)
  else:
#    print(pi)
    pis=[]
    #for i in pi:
      #pis.append(Graph.edge_subgraph(i))
      #pis.append(Graph.subgraph(i))
    pis.append(pi)
    b=l
    l=(a+b)/2

for i in pis[0]:
  #print(i.edges())
  print(i)



#print(Graph.edges(data=True))
#nx.draw(GraphML)
#plt.show()