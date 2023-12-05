## Topology

%definition% 

A datatype containing ordered list of references to other features. 

Other features may be either features with topology properties or GeoJSON (or FG-JSON) point objects.

This is a generalisation of the TopoJSON concept using inline data, and not limited to linestrings.

Note this requires JSON-LD V1.1 processing to handle nested arrays of references for Polygons etc.

