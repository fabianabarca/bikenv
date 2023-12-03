import bikenv
import keys


GOOGLE_API_KEY = keys.GOOGLE_API_KEY
region_query = "New York, United States of America"

# Create a region object
# Get the indexes of the region of interest
region = bikenv.Region(query = region_query,
                    google_api_key=GOOGLE_API_KEY, bbox_dist=300)
print("This is the graph of the region of interest.")
# Print(f"Object: {type(region)}.")

# Obtain altitude stats
mean, var, std, skew, kurt = region.elevation_stats()

# Print altitude index
print(region.elevation_mean)
print(region.altitude_index_var)
print(region.altitude_index_std)

# Print distance index
print(region.distance_index)

# Plot region
region.plot_region()

# Plot elevation
region.plot_elevation()

# Plot normalized elevation histogram   
region.normalized_elevation_hist()
