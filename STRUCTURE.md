# Structure of the package

`class` **Region**

- Attributes
    - `name`
    - `google_api_key`
    - `G`
    - `altitude_index`
    - `distance_index`
    - `normalized_elevations`
- Methods
    - `_get_region()`


```mermaid
---
title: bikenv
---
classDiagram
    class Region{
        +string name
        -string google_api_key
        +NetworkX-DiGraph G
        +float altitude_index
        +float distance_index
        +GeoDataFrame normalized_elevations
        +plot_region()
        -_get_region()
    }
```