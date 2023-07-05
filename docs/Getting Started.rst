Getting Started
==========

This is the description of the module.

Get Started
-----------
- Install Bikenv following the installation guide.
- Read the information about the package.
- Follow the example.
- Refer to the function structure in the references.

Essentially, this package should work by knowing the city you want to analyze, the type of data you want to work with, in our case it would be "drive" as we want to gather street information, and if you have a Google API, you can enter the code to access elevation information to be analyzed by the same package.


Libraries
--------------
This package works with various libraries, the list would be:

- Osmnx
- Networkx
- Numpy
- Pandas
- Geopandas
- Spicy.Stats
- Matplotlib.pyplot


As part of the package development, we worked with Osmnx's example notebooks to extract geographic information from Open Street Maps and process it.


Configuration
--------------
One of the configurations that can be used is that the package is pre-designed to work with geographical road information, but by changing the "drive" parameter, it can be used to study and analyze other types of data for different purposes.

On the other hand, the package assumes that the user already has a Google API to obtain updated elevation information. However, it is known that not every user necessarily has this API. Depending on whether the user has this API or not, they can obtain the elevation index or not. If the API is not available, the elevation cannot be obtained.

Results
--------------
The expected results for this package are two indicators as mentioned in about.rst and a histogram where the differences in distances can be visualized. As an additional feature, by modifying the code, geographic maps can be obtained with information nodes plotted. Centrality can be graphed using colors, as well as the routes that can be taken between different points, and nodes with higher or lower elevation can be highlighted.

Use Example
-----------

.. code-block:: python

   import geopandas
   import bikenv

   # Create the network multidigraph of the city
   G = bikenv.get_region(San José, drive) 

   #Calculate the index of altitude
   # Obtain the altitud data.
   alturas_equiv = bikenv.altitude_index(G, google_key)

   #Obtain the stats of the altitude
   variances = bikenv.stats(alturas_equiv)

   #Calculate the index of distance
   second_index = bikenv.distance_index(G)


.. important::
   The documentation is under construction.

.. automodule:: bikenv.module
   :members:
   :undoc-members:
   :show-inheritance:
