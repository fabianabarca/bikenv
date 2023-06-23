import osmnx as ox
import networkx as nx
from scipy.stats import skew
from scipy.stats import kurtosis


def get_region(text: str, networktype: str):
    """Get the region from OSM as a graph.

    Parameters
    ----------
    region : string
        The name of the region to get from OSM
    network_type : string
        The type of network to get from OSM. Default is 'drive'

    Returns
    -------
    G : networkx multidigraph
    """
    G = ox.graph_from_place(text, network_type=networktype)
    fig, ax = ox.plot_graph(G)  # Para graficar, se puede modificar
    return G

def altitude_index(G, google_key: str):
    """Calculate the index of a graph based on the altitude of the nodes.

    Parameters
    ----------
    G : networkx multidigraph
        The graph to calculate the index
    google_key : string
        The key to use the Google Elevation API

    Returns
    -------
    alturas_equiv : one-dimensional data structure
        The elevation data prepared to be compared and analized
    """
    # Obtain the elevation of all nodes
    try:
        G = ox.elevation.add_node_elevations_google(G, api_key=google_key)
        G = ox.elevation.add_edge_grades(G)
        nc = ox.plot.get_node_colors_by_attr(G, "elevation", cmap="plasma")
        fig, ax = ox.plot_graph(
            G, node_color=nc, node_size=20, edge_linewidth=2, edge_color="#333"
        )
    except ImportError:
        print("You need a google_elevation_api_key to run this cell.")

    gdf = ox.graph_to_gdfs(G)
    ele = gdf[0]["elevation"]

    promedio = np.mean(ele)

    alturas_equiv = ele - promedio

    return alturas_equiv

def stats(alturas_equiv):

    """ Obtain important stats form de data provided.

    Parameters
    ----------
    alturas_equiv : one-dimensional data structure

    Returns
    -------
    variances : variance of alturas_equiv
    std : std of alturas_equiv
    sesgo : skew of alturas_equiv
    kurt : kurtosis of alturas_equiv
    """

    print("Los datos obtenidos de la elevación de la ciudad son: \n")
    
    variances = np.var(y) #Varianza
    print("La varianza es:",variances)
    
    std = np.std(y)
    print("La desviación estandar es:",std)
    
    sesgo = skew(y)
    print("El sesgo es:",sesgo)

    kurt = kurtosis(y)
    print("La kurtosis es:",kurt)

    return variances, std, sesgo, kurt    

def hist(list_data):

    """ Obtain important stats form de data provided.

    Parameters
    ----------
    list_data : list of two o more one-dimensional data structures.

    Returns
    -------
    graph : histograms of all data lists in the same graph.
    """

    num_bins = 50  # Número de divisiones del histograma
    for i in x:
        plt.hist(i, bins=num_bins, edgecolor='black', density=True)
        

    # Configurar etiquetas y título
    plt.xlabel('Diferencia con respecto a la altitud media (m)')
    plt.ylabel('Densidad')
    plt.title('Histograma de altitud de nodos de una ciudad')

    # Mostrar el histograma
    plt.show()

#--------------------------
#Distance_index
def distance_index(G):

    def shortestroad_distance(G):

        """ Obtain a matrix with all the distances on road in meters between all nodes of G.

        Parameters
        ----------
        G : networkx multidigraph
        The graph to calculate the index

        Returns
        -------
        shortestdistance : list of lists matrix. 
        Distances between all nodes. Each list is de distances form one node to all nodes.
        """
        gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
        num_filas = len(gdf_nodes)
        shortestdistance = []

        for i in range(num_filas): #Se obtiene el nodo de origen
            data = gdf_nodes.iloc[i]
            longitud = data["y"]
            latitud = data["x"]
            orig = ox.distance.nearest_nodes(G, X=latitud, Y=longitud)
            shortestdistance1 = []
            for j in range(num_filas): #Se obtiene el nodo destino, que serían todos los nodos
                data = gdf_nodes.iloc[j]
                longitud = data["y"]
                latitud = data["x"]
                dest = ox.distance.nearest_nodes(G, X=latitud, Y=longitud)
                route = ox.shortest_path(G, orig, dest, weight="travel_time") #Se obtiene la ruta para ese orig y dest
                if route is not None: #Si la ruta existe se obtiene la distancia de esa ruta
                    edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, "length")
                    dist = round(sum(edge_lengths)) #Se redondea para obtener número de metros
                    shortestdistance1.append(dist)
                else: 
                    break
            shortestdistance.append(shortestdistance1)
                
        #print("distancias entre todos los nodos por calles: \n", shortestdistance)
        road_matrix = np.array(shortestdistance)

        return road_matrix

    def shortestcrow_distance(G):
        """ Obtain a matrix with all the distances in straight line in meters between all nodes of G.

        Parameters
        ----------
        G : networkx multidigraph
        The graph to calculate the index

        Returns
        -------
        shortestcrowdistance : matrix. 
        Distances between all nodes. Each list is de distances form one node to all nodes in a straight line.
        """
        gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
        num_filas = len(gdf_nodes)
        shortestcrowdistance = []

        for i in range(num_filas): #Se obtiene el nodo de origen
            data = gdf_nodes.iloc[i]
            orig_y = data["y"]
            orig_x = data["x"]
            #print(orig_x)
            orig = ox.distance.nearest_nodes(G, X=latitud, Y=longitud)
            shortestcrowdistance1 = []
            for j in range(num_filas): #Se obtiene el nodo destino, que serían todos los nodos
                data = gdf_nodes.iloc[j]
                dest_y = data["y"]
                dest_x = data["x"]
                dest = ox.distance.nearest_nodes(G, X=latitud, Y=longitud)
                dist2 = round(ox.distance.great_circle_vec(orig_y, orig_x, dest_y, dest_x))
                #print(dist2)
                shortestcrowdistance1.append(dist2)

            shortestcrowdistance.append(shortestcrowdistance1)

        #print("distancia en linea recta entre todos los nodos: \n", shortestcrowdistance)
        crow_matrix = np.array(shortestcrowdistance)


        return crow_matrix

    def divide_matrix(matrix1, matrix2):
        """ Obtain matrix, dividen each value from matrix1 with the corresponding value from matrix2.

        Parameters
        ----------
        matrix1 : matrix with all distances on road of all nodes.
        matrix2 : matrix with all distances on straignt line of all nodes.

        Returns
        -------
        dist_result : matrix with the results of the division 
        """
        dist_result = np.nan_to_num(np.divide(matrix1, matrix2, where=matrix2!=0)) 

        return dist_result

    def row_mean(matrixreslt):
        """ Calculate the mean of each row in a matrix.

        Parameters
        ----------
        matrixreslt : matrix.
            The matrix generated by the division of both distances calculated.

        Returns
        -------
        avarage_matrix : list with the means of each row.
        """
        row_averages = np.mean(dist_result, axis=1)
        average_matrix = np.array([row_averages]).T #Promedios de cada una de las filas

        return average_matrix

    def mean_of_means(means): 
        """ Calculate the mean of each value in a list.

        Parameters
        ----------
        means : list.
            List one-dimensional data structure.

        Returns
        -------
        secondindex : Mean of all values in a list.
        """
        secondindex = np.mean(average_matrix) #Obtención del segundo índice

        return secondindex
    
    road_matrix = shortestroad_distance(G)
    crow_matrix = shortestcrow_distance(G)
    dist_result = divide_matrix(road_matrix, crow_matrix)
    average_matrix = row_mean(dist_result)
    second_index = mean_of_means(average_matrix)

    return second_index
    