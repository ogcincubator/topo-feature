## Feature with explicit Topology

A feature type using a topology property to reference an ordered list of references to other features. 

Other features may be either features with topology properties or GeoJSON (or FG-JSON) point objects.

This is a generalisation of the TopoJSON concept using inline data, (nested sets of coordinates) but not limited to the LineStrings. Topological defined objects 
can be solids, swept volumes or any other concept. (It doesnt use TopoJSON coordinate compaction and transformation, however it does allow for explicit CRS, and coordinate compaction transformations could be defined as derived CRS if required.)

