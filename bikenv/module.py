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
        self.google_api_key = google_key
        self.G = self._get_region()
        self.normalized_elevations, self.elevation_mean = self._normalize_elevation()
        self.altitude_index = self._altitude_index()
        self.distance_index = self._distance_index()

    def plot_region(self):
        """Plot the region from OSM as a graph.

        Parameters
        ----------
        self.G : networkx multidigraph
            The region networkx multidigraph

        Returns
        -------
        Region plot
        """
        try:
            _, _ = ox.plot_graph(self.G)
        except:
            print(f"OSM could not find '{self.name}' graph.")
            print("Please try again with a different region.")

    def plot_elevation(self):
        """Plot the region from OSM as a graph.

        Parameters
        ----------
        self.G_elevation : networkx multidigraph
            The region networkx multidigraph with elevation nodes and edges
        self.nc : node colors
            The color for each node

        Returns
        -------
        Region altitude plot
        """
        try:
            _, _ = ox.plot_graph(
                self.G_elevation,
                node_color=self.nc,
                node_size=20,
                edge_linewidth=2,
                edge_color="#333",
            )
        except:
            print(f"OSM could not find '{self.name}' elevation graph.")
            print("Please try again with a different region.")

    def elevation_stats(self):
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
        try:
            print("Los datos obtenidos de la elevación de la ciudad son: \n")

            mean = self.elevation_mean
            print("La media es:", mean)

            var = np.var(self.normalized_elevations)  # Varianza
            print("La varianza es:", var)

            std = np.std(self.normalized_elevations)
            print("La desviación estandar es:", std)

            skew = stats.skew(self.normalized_elevations)
            print("El sesgo es:", skew)

            kurt = stats.kurtosis(self.normalized_elevations)
            print("La kurtosis es:", kurt)

            return mean, var, std, skew, kurt
        except:
            return None, None, None, None, None

    def normalized_elevation_hist(self):
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
        try:
            num_bins = 50

            for i in self.normalized_elevations:
                plt.hist(i, bins=num_bins, edgecolor="black", density=True)

            plt.xlabel("Difference with respect to mean altitude (m)")
            plt.ylabel("Density")
            plt.title(
                "Histogram to compare normalized elevation of two or more regions.")
            plt.show()
        except:
            print("Not able to show normalized elevation histogram")

    def _get_region(self):
        """Get the region from OSM as a graph.

        TODO: How to limit the region, for example, to a circular area of N km radius around the center of the region. This is to avoid getting a graph that is too big. Search for other options to "trim" the graph by dead ends or other criteria so that distances are not distorted.

        Parameters
        ----------
        region : string
            The name of the region to get from OSM

        Returns
        -------
        G : networkx multidigraph
        """
        try:
            G = ox.graph_from_place(self.name, network_type="drive")
            return G
        except:
            print(f"OSM could not find '{self.name}'.")
            print("Please try again with a different region.")
            return None

    def _normalize_elevation(self):
        """Calculates the altitude index of a graph based on the altitude of the nodes.

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
        try:
            # Obtain the elevation of all nodes
            try:
                self.G_elevation = ox.elevation.add_node_elevations_google(
                    self.G, api_key=self.google_api_key
                )
                self.G_elevation = ox.elevation.add_edge_grades(self.G)
                self.nc = ox.plot.get_node_colors_by_attr(
                    self.G, "elevation", cmap="plasma"
                )

            except:
                if (self.G != None):
                    print("You need a google_elevation_api_key to run this cell.")

            gdf = ox.graph_to_gdfs(self.G)

            # Get and normalize the elevation data
            elevation = gdf[0]["elevation"]
            elevation_mean = np.mean(elevation)
            normalized_elevations = elevation - elevation_mean

            return normalized_elevations, elevation_mean
        except:
            return None, None

    def _altitude_index(self):
        try:
            index = self._normalize_elevation()
            return index
        except:
            return None

    def _distance_index(self):
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
        try:

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
                        dest = ox.distance.nearest_nodes(
                            G, X=latitud, Y=longitud)
                        route = ox.shortest_path(
                            G, orig, dest
                        )  # Se obtiene la ruta para ese orig y dest

                        # If origin and destination are the same node then route is set to None
                        if orig == dest:
                            route = None

                        if (
                            route is not None
                        ):  # Si la ruta existe se obtiene la distancia de esa ruta
                            dist = round(
                                sum(
                                    ox.utils_graph.route_to_gdf(G, route, "length")[
                                        "length"
                                    ]
                                )
                            )  # Se redondea para obtener número de metros
                            shortestdistance1.append(dist)
                            # _, _ = ox.plot_graph_route(G, route, route_color="y", route_linewidth=6, node_size=0)
                        else:
                            # If route is None zero is appended
                            selfdistance = 0
                            shortestdistance1.append(selfdistance)
                            pass
                        # print(shortestdistance1)
                    shortestdistance.append(shortestdistance1)

                # print(shortestdistance.tail())

                # print("distancias entre todos los nodos por calles: \n", shortestdistance)
                road_matrix = np.array(shortestdistance)

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
                            ox.distance.great_circle_vec(
                                orig_y, orig_x, dest_y, dest_x)
                        )
                        # print(dist2)
                        shortestcrowdistance1.append(dist2)

                    shortestcrowdistance.append(shortestcrowdistance1)

                # print("distancia en linea recta entre todos los nodos: \n", shortestcrowdistance)
                crow_matrix = np.array(shortestcrowdistance)

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
                dist_result = np.nan_to_num(
                    np.divide(matrix1, matrix2, where=matrix2 != 0))

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
                secondindex = np.mean(
                    average_matrix)  # Obtención del segundo índice

                return secondindex

            road_matrix = shortestroad_distance(self.G)
            crow_matrix = shortestcrow_distance(self.G)
            dist_result = divide_matrix(road_matrix, crow_matrix)
            average_matrix = row_mean(dist_result)
            second_index = mean_of_means(average_matrix)

            return second_index
        except:
            return None
