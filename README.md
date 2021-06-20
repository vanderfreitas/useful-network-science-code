# Network science code


The networks used in each algorithm is in **networks** folder and its name is passed through command line. For example, within the **metrics** folder, 
`python local_metrics.py fluvial`
runs all sorts of metrics for the network in *networks/fluvial.GraphML*

## networks: 
Network examples in GraphML file format.
- **terrestrial.GraphML**: Terrestrial network from IBGE 2016...
- **fluvial.GraphML**: Fluvial network from IBGE 2016...
- **aerial.GraphML**: ... ANAC
- **aerialUTP.GraphML**: ... ANAC aggregated into UTP...

## create_network:
Scripts to create networks from data and known algorithms.
- **generate_fluvial_and_terrestrial_networks_from_IBGE_2016.py**: 
- **mobility_filter_cities.py**:

## metrics:
Local and global metrics for undirected and (un)weighted networks.
- **global_metrics.py**:
- **local_metrics.py**:

## data_conversion:
Useful data conversions. Example: from GraphML to shapefile.


## thresholding:
Methods to threshold weighted networks.
- **thresholding.py**:
- **threshold_based_on_maximum_diameter.py**:
- **backbone.py**: