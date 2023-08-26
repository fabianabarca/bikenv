import bikenv
import keys

GOOGLE_API_KEY = keys.GOOGLE_API_KEY

print("This is an example of how to use the package.")

# Get the graph of the region of interest
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


# With OOP:

# Create a region object
tibas = bikenv.Region("Cinco Esquinas de Tibás, San José, Costa Rica", google_key="")
print("This is the graph of the region of interest.")

# Get the indexes of the region of interest
tibas.altitude_index
tibas.distance_index

# Get the stats of the altitude index (possibly must change in the future)
tibas.normalized_elevation_stats()

# Plot the histogram of the altitude index
tibas.normalized_elevation_hist()