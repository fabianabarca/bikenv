import bikenv
import keys


GOOGLE_API_KEY = keys.GOOGLE_API_KEY

print("This is an example of how to use the package.")

"""# Get the graph of the region of interest
G = bikenv.get_region("Cinco Esquinas de Tibás, San José, Costa Rica")

print("This is the graph of the region of interest.")

# Get the altitude index of the region of interest
normalized_elevation = bikenv.altitude_index(G, google_key=GOOGLE_API_KEY)

print("This is the altitude index of the region of interest.")

# Get the stats of the altitude index
stats = bikenv.normalized_elevation_stats(normalized_elevation)

print("Stats of the altitude index of the region of interest.")
print(stats)

# Plot the histogram of the altitude index
bikenv.normalized_elevation_hist(normalized_elevation)

# Get the distance_index
distance_index = bikenv.distance_index(G)
print("This is the distance index")
print(distance_index)
"""
""
# With OOP:

# Create a region object
region = bikenv.Region("New York, United States of America",
                       google_api_key=GOOGLE_API_KEY, bbox_dist=300)
print("This is the graph of the region of interest.")
# print(f"Object: {type(region)}.")

# Get the indexes of the region of interest
# print(region.normalized_elevations)
print('Distance Index:')
# print(region.distance_index)
region.plot_region()
region.plot_elevation()

'''
print(tibas.elevation_stats())
region.normalized_elevation_hist()
Get the stats of the altitude index (possibly must change in the future)
region.normalized_elevation_stats()

Plot the histogram of the altitude index
region.normalized_elevation_hist()
'''
