"""
User Reference.

==========
This guide describes the use of all the functions used in the package for reference purposes. All these functions can be accessed through bikenv.module_name.function_name(). This package uses different libraries that need to be installed before using it to avoid errors.
"""

import numpy as np
from scipy import stats
import osmnx as ox
import matplotlib.pyplot as plt


# TODO: class Region with attributes: name, graph, altitude_index, distance_index, and methods: normalized_elevation_stats, normalized_elevation_hist

class Region:
    def __init__(self, name: str, google_key: str):
        self.name = name
        self.graph = get_region(name)
        self.altitude_index = altitude_index(self.graph, google_key)
        self.distance_index = distance_index(self.graph)


def get_region(text: str):
    """Get the region from OSM as a graph.

    Parameters
    ----------
    region : string
        The name of the region to get from OSM

    Returns
    -------
    G : networkx multidigraph
    """
    try:
        G = ox.graph_from_place(text, network_type="drive")
        _, _ = ox.plot_graph(G)
        return G
    except:
        print(f"OSM could not find '{text}'.")
        print("Please try again with a different region.")
    

def altitude_index(G, google_key: str):
    """Calculate the altitude index of a graph based on the altitude of the nodes.

    Parameters
    ----------
    G : networkx multidigraph
        The graph to calculate the index
    google_key : string
        The key to use the Google Elevation API

    Returns
    -------
    normalized_elevation : one-dimensional data structure
        The elevation data prepared to be compared and analized
    """
    # Obtain the elevation of all nodes
    try:
        G = ox.elevation.add_node_elevations_google(G, api_key=google_key)
        G = ox.elevation.add_edge_grades(G)
        nc = ox.plot.get_node_colors_by_attr(G, "elevation", cmap="plasma")
        _, _ = ox.plot_graph(
            G, node_color=nc, node_size=20, edge_linewidth=2, edge_color="#333"
        )
    except ImportError:
        print("You need a google_elevation_api_key to run this cell.")

    gdf = ox.graph_to_gdfs(G)
    
    # Get and normalize the elevation data
    elevation = gdf[0]["elevation"]
    elevation_mean = np.mean(elevation)
    normalized_elevation = elevation - elevation_mean

    return normalized_elevation


def normalized_elevation_stats(normalized_elevation):
    """
    Obtain basic stats from the data provided.

    Parameters
    ----------
    normalized_elevation : one-dimensional data structure

    Returns
    -------
    variances : variance of normalized elevation data
    std : standard deviation of normalized elevation data
    sesgo : skewness of normalized elevation data
    kurt : kurtosis of normalized elevation data
    """
    print("Los datos obtenidos de la elevación de la ciudad son: \n")

    var = np.var(normalized_elevation)  # Varianza
    print("La varianza es:", var)

    std = np.std(normalized_elevation)
    print("La desviación estandar es:", std)

    skew = stats.skew(normalized_elevation)
    print("El sesgo es:", skew)

    kurt = stats.kurtosis(normalized_elevation)
    print("La kurtosis es:", kurt)

    return var, std, skew, kurt


def normalized_elevation_hist(region_data):
    """
    Histogram to compare normalized elevation of two or more regions.

    TODO: Add a legend to the graph.

    Parameters
    ----------
    list_data : list of two o more one-dimensional data structures.

    Returns
    -------
    graph : histograms of all data lists in the same graph.
    """
    num_bins = 50
    
    for i in region_data:
        plt.hist(i, bins=num_bins, edgecolor="black", density=True)

    plt.xlabel("Difference with respect to mean altitude (m)")
    plt.ylabel("Density")
    plt.title("Histogram to compare normalized elevation of two or more regions.")
    plt.show()


def distance_index(G):
    """
    Get the index related to distances.

    Parameters
    ----------
    G : networkx multidigraph
        The graph to calculate the index

    Returns
    -------
    distanceindex : value of the index.
    """

    def shortestroad_distance(G):
        """
        Obtain a matrix with all the distances on road in meters between all nodes of G.

        Parameters
        ----------
        G : networkx multidigraph
        The graph to calculate the index

        Returns
        -------
        shortestdistance : list of lists matrix.
        Distances between all nodes. Each list is de distances form one node to all nodes.
        """
        gdf_nodes = ox.graph_to_gdfs(G)[0]
        num_filas = len(gdf_nodes)
        shortestdistance = []

        for i in range(num_filas):  # Se obtiene el nodo de origen
            data = gdf_nodes.iloc[i]
            longitud = data["y"]
            latitud = data["x"]
            orig = ox.distance.nearest_nodes(G, X=latitud, Y=longitud)
            shortestdistance1 = []
            for j in range(
                num_filas
            ):  # Se obtiene el nodo destino, que serían todos los nodos
                data = gdf_nodes.iloc[j]
                longitud = data["y"]
                latitud = data["x"]
                dest = ox.distance.nearest_nodes(G, X=latitud, Y=longitud)
                route = ox.shortest_path(
                    G, orig, dest
                )  # Se obtiene la ruta para ese orig y dest

                #If origin and destination are the same node then route is set to None
                if orig == dest:
                    route = None
                
                
                if (
                    route is not None
                ):  # Si la ruta existe se obtiene la distancia de esa ruta
                    
                    dist = round(
                        sum(
                            ox.utils_graph.route_to_gdf(G, route, "length")["length"]
                        )
                    )  # Se redondea para obtener número de metros
                    shortestdistance1.append(dist)
                    #_, _ = ox.plot_graph_route(G, route, route_color="y", route_linewidth=6, node_size=0)
                else:
                    #If route is None zero is appended
                    selfdistance = 0
                    shortestdistance1.append(selfdistance)
                    pass
                #print(shortestdistance1)
            shortestdistance.append(shortestdistance1)
        
        #print(shortestdistance.tail())

        # print("distancias entre todos los nodos por calles: \n", shortestdistance)
        road_matrix = np.array(shortestdistance)
        print(road_matrix.shape)

        return road_matrix

    def shortestcrow_distance(G):
        """
        Obtain a matrix with all the distances in straight line in meters between all nodes of G.

        Parameters
        ----------
        G : networkx multidigraph
        The graph to calculate the index

        Returns
        -------
        shortestcrowdistance : matrix.
        Distances between all nodes. Each list is de distances form one node to all nodes in a straight line.
        """
        gdf_nodes = ox.graph_to_gdfs(G)[0]
        num_filas = len(gdf_nodes)
        shortestcrowdistance = []

        for i in range(num_filas):  # Se obtiene el nodo de origen
            data = gdf_nodes.iloc[i]
            orig_y = data["y"]
            orig_x = data["x"]
            # print(orig_x)
            orig = ox.distance.nearest_nodes(G, X=orig_x, Y=orig_y)
            shortestcrowdistance1 = []
            for j in range(
                num_filas
            ):  # Se obtiene el nodo destino, que serían todos los nodos
                data = gdf_nodes.iloc[j]
                dest_y = data["y"]
                dest_x = data["x"]
                dest = ox.distance.nearest_nodes(G, X=dest_y, Y=dest_x)
                dist2 = round(
                    ox.distance.great_circle_vec(orig_y, orig_x, dest_y, dest_x)
                )
                # print(dist2)
                shortestcrowdistance1.append(dist2)

            shortestcrowdistance.append(shortestcrowdistance1)

        # print("distancia en linea recta entre todos los nodos: \n", shortestcrowdistance)
        crow_matrix = np.array(shortestcrowdistance)
        print(crow_matrix.shape)
        return crow_matrix

    def divide_matrix(matrix1, matrix2):
        """
        Obtain matrix, dividen each value from matrix1 with the corresponding value from matrix2.

        Parameters
        ----------
        matrix1 : matrix with all distances on road of all nodes.
        matrix2 : matrix with all distances on straignt line of all nodes.

        Returns
        -------
        dist_result : matrix with the results of the division
        """
        dist_result = np.nan_to_num(np.divide(matrix1, matrix2, where=matrix2 != 0))

        return dist_result

    def row_mean(matrixreslt):
        """
        Calculate the mean of each row in a matrix.

        Parameters
        ----------
        matrixreslt : matrix.
            The matrix generated by the division of both distances calculated.

        Returns
        -------
        avarage_matrix : list with the means of each row.
        """
        row_averages = np.mean(dist_result, axis=1)
        average_matrix = np.array(
            [row_averages]
        ).T  # Promedios de cada una de las filas

        return average_matrix

    def mean_of_means(means):
        """
        Calculate the mean of each value in a list.

        Parameters
        ----------
        means : list.
            List one-dimensional data structure.

        Returns
        -------
        secondindex : Mean of all values in a list.
        """
        secondindex = np.mean(average_matrix)  # Obtención del segundo índice

        return secondindex

    road_matrix = shortestroad_distance(G)
    crow_matrix = shortestcrow_distance(G)
    dist_result = divide_matrix(road_matrix, crow_matrix)
    average_matrix = row_mean(dist_result)
    second_index = mean_of_means(average_matrix)

    return second_index
