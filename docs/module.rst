The module
==========

This is the description of the module.

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
