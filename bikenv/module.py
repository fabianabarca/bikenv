"""Hola."""

import osmnx as ox
import networkx as nx


def get_region(name, network_type="drive"):
    """Get the region from OSM as a graph.

    Parameters
    ----------
    region : string
        The name of the region to get from OSM
    network_type : string
        The type of network to get from OSM. Default is 'drive'

    Returns
    -------
    road_network : networkx multidigraph
    """
    road_network = "Hola"
    return road_network


def altitude_index(G, google_key):
    """Calculate the index of a graph based on the altitude of the nodes.

    Parameters
    ----------
    G : networkx multidigraph
        The graph to calculate the index
    google_key : string
        The key to use the Google Elevation API

    Returns
    -------
    index : float
        The index of the graph
    """
    index = 24.5
    index = index/2
    return index


def distance_index(G):
    """Calculate the index of a graph based on the distance of the nodes.

    Parameters
    ----------
    G : networkx multidigraph
        The graph to calculate the index

    Returns
    -------
    index : float
    
    """
    index = 1849
    return index
