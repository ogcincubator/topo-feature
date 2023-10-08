# Features with topology

This repository defines an extension to GeoJSON or FG-JSON definining topological relationships between features based on identifiers.

The set of components are listed [here](https://ogcincubator.github.io/topo-features/)

The implementation provides a JSON schema and a corresponding JSON-LD context that can turn topology references into object properties.

Topological consistency functions can be described using SHACL rules - for example that a Polygon geometry must reference LineStrings, and Linestrings must reference Point objects. 

This is extensible (unlike topoJSON) and can span features across any collection schemas used to group them.

Using features rather than geometries as the topology reference allows arbitrary additional metadata to be provided about the nature of boundaries between features.

NB. GeoJSON simple geometries and TopoJSON compact topologies can be derived from the model if required.

[More information on design and usage](https://github.com/opengeospatial/bblock-template/blob/master/USAGE.md)


