The module
==========

This is the description of the module.

Use Example
-----------

.. code-block:: python

   import geopandas
   import bikenv

   # Read the shapefile of the boundary of San Jose
   sanjose_boundary = geopandas.read_file('sanjose_boundary.shp')

   # Create a Region object
   sanjose = bikenv.Region(sanjose_boundary)

   # Get the altitude index
   alt_index = sanjose.get_index_altitude()

   # Get the distance index
   dis_index = sanjose.get_index_distance()

.. important::
   The documentation is under construction.

.. automodule:: bikenv.module
   :members:
   :undoc-members:
   :show-inheritance:
