## Feature Collection with Explicit Topology 

%definition% 

A Feature Collection where the set of TopoFeatures contained describe the full geometry of higher-dimension features by topology relationships, ultimately grounded in Point features with explicit coordinates.

TopoFeature is feature type using a topology property to reference an ordered list of references to other features. 

Other features may be either features with topology properties or GeoJSON (or FG-JSON) point objects.

This is a generalisation of the TopoJSON concept using inline data, but not limited to the LineStrings. Topological defined objects 
can be solids, swept volumes or any other concept.

