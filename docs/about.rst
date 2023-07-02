About the package
=================
As a result of the initial stages of the research, a Python package is expected to provide tools for the measurements of the proposal. This package is proposed to be called bikenv (biking environment) and should be made available as free software in PyPI (Python Package Index) with documentation in Read the Docs.

It explores some environmental factors of a region -- namely natural features like the topography, and climate and built features like the vehicle road network -- that affect cycling.

This package allows users to use tools to discover physical characteristics of cities through two indices that provide information about the ease or difficulty for cyclists to navigate the city. This package arises from the need to learn about city characteristics worldwide.

On the planet, millions of people use bicycles daily to commute to their workplaces, schools, universities, and other destinations. Therefore, the information obtained or the package's code implementation can be highly beneficial for cyclists and individuals with future projects related to geographic analysis of cities, including elevation and distances.

The package utilizes various libraries to achieve the desired results. Currently, it operates through Osmnx and Networkx, which enable access to free geographic information from OpenStreetMap and perform measurements between the obtained information points.

Through a simple search function, these packages retrieve information nodes at each intersection and dead-end street in the studied city or area. This process can yield hundreds or even thousands of nodes, depending on the requested zone's size, although this might affect the package's analysis time to some extent. From these nodes, the desired information is extracted, and necessary analyses are conducted to obtain the indicators.

Indexes
=================

One of the main objectives is to obtain two indicators that provide insights into the studied city:

-*Altitude-index:*
This indicator relates to changes in altitude within a city. It is important to consider because cyclists face more difficulty moving in areas with significant elevation changes due to the physical effort required. The goal of this indicator is to capture the variance in altitudes among all the information points in the studied zone.


-*Distance-index:*
This indicator takes into account both the nearest road distance and the straight-line distance between each pair of information nodes. The results are divided and averaged to obtain a number that provides information about the ease or difficulty of reaching each point as a cyclist.

.. math::

   C = \frac{{\text{{shortest distances on road from one node}}}}{{\text{{shortest distances to all nodes from one node on straight line}}}}


Data Types
=================
*GIS*
^^^^^^^^^^^^^^^^^^^
The geographic information system (GIS) captures, stores, verifies, and displays geographic information of a location. The information that this system works with includes vector data and raster data.

Vector Data
+++++++++++++++++++

This is the most commonly used type of information in programs such as Open Street Map and Google Maps. This type of information consists of points, lines, and polygons.

Points: Represent distinctive points of information, such as a particular place, a city, or points of interest.
Lines: Gives information about streets or rivers. It has a starting point and an ending point and can be used to measure lengths.
Polygons: Represent areas of cities, forests, or lakes. It can measure area perimeters due to having two dimensions.

Raster Data
+++++++++++++++++++


In this type of information, pixels can be worked on as each one represents a value. This type of information can be found in satellites or topographic maps.

There are two types of raster data:

Continuous Data: Points in the grid cells that change gradually.
Discrete Data: Can take a limited set of values. For example, each pixel can have various discrete values that represent different types of land use, such as forests, urban areas, farmland, etc.

GeoPandas
^^^^^^^^^^^^^^^^^^^
The geopandas data structure consists of GeoSeries and GeoDataFrame.

GeoSeries
+++++++++++++++++++

A GeoSeries is a vector of information, similar to a series in Pandas. In geopandas, it has three classes of objects:

-Points/MultiPoints

-Lines/MultiLines

-Polygons/MultiPolygons

This information can be used to obtain the area, boundaries, or geometry type. Additionally, it allows you to calculate distances between objects, find the center of an object, or plot information.

GeoDataFrame
+++++++++++++++++++

A GeoDataFrame is another type of geopandas structure that consists of multiple GeoSeries organized in a tabular form. Each row represents a geospatial object, and each column represents a feature associated with that object. It provides a convenient way to store and analyze geospatial data, combining both geometric and attribute information.

GeoJSON
^^^^^^^^^^^^^^^^^^^
GeoJSON is a format for encoding a variety of geographic data structures.

GeoJSON supports the following types of entities:

-Points (including addresses and locations)

-Text strings (including addresses, roads, and boundaries)

-Polygons (including countries, provinces, and land masses)

-Multi-part collections of point entities, text strings, or polygons.

In essence, GeoJSON is an open data interchange format that represents simple geographic entities and their non-spatial attributes.
