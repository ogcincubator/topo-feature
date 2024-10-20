# 3D Geometries and topologies for Cadastral representation

<!--
:Author:    Andrew Hunter
:Email:     <andrew@edgegeomatics.co.nz>
:Date:      4 December 2023
:Updated:   
:Revision:  0.2

:History: 
:Ver 0.1: Initial draft of document
:Ver 0.2: Generalised as documentation for topo-feature Building Blocks.

-->

#### Table of Contents

1. [Introduction](#introduction)
2. [Proposed JSON-FG 3D Geometries](#proposed-json-fg-3d-geometries)
   1. [Polyhedron](#polyhedron)
   2. [MultiPolyhedron](#multipolyhedron)
   3. [Prism](#prism)
   4. [MultiPrisim](#multiprisim)
3. [Definitions](#definitions)
   1. [Points](#points)
   2. [Curves & Polygons](#curves-and-polygons)
   3. [Polyhedron](#polyhedron-1)
   4. [MultiPolyhedron](#multipolyhedron-1)
   5. [Prism](#prism-1)
   6. [MultiPrism](#multiprism-1)
   7. [Swept Path](#sweptpath)
4. [Draft Outline of Potential 3D Geometry Operations](#3d-geometry-operators)
5. [References](#references)



## Introduction

GeoJSON [[1]](#1) adopts seven geometry types defined in
OGCs [Simple Features Specification for SQL Rev 1.1](https://portal.ogc.org/files/?artifact_id=829). The specification does not officially support 3D geometries. 
GeoJSON has been designed to represent simple spatial features, and it primarily deals with 2D geometries. However, 
there have been discussions and proposals within the geospatial community to extend GeoJSON to support 3D geometries, 
including the addition of properties to represent elevation. Some unofficial extensions or variations of GeoJSON may 
include 3D features, but they are not part of the official GeoJSON standard.

A recent proposal [[2]](#2) by OGC's Features and Geometries JSON (JSON-FG) Software Working Group has proposed support for 
**solid** and **multi-solid** geometries. JSON-FG proposes <code>Polyhedron</code>, <code>MultiPolyhedron</code>, 
<code>Prism</code>, and <code>MultiPrism</code>.

Most 3D geometries stored in databases are encoded in WKT/WKB [[3]](#3), which allows <code>ST_Solid</code> and 
<code>ST_BRepSolid</code>. PostGIS [[4]](#4) supports a <code>PolyhedralSurface</code> that can be converted to a solid 
(ST_MakeSolid). A cursory search for implementations of <code>ST_Solid</code> and <code>ST_BRepSolid</code> revealed no 
opensource libraries that implement these geometries. It is recognised that there are proprietary solutions, 
particularly within the CAD and computational geometry domains.


## Proposed JSON-FG 3D Geometries

### Polyhedron

A <code>Polyhedron</code> is a <code>solid</code> defined by a set of bounding surfaces. Each bounding surface is a 
closed simple surface, often called a <code>Shell</code>. Each <code>solid</code> has a unique exterior 
<code>Shell</code> and potentially a set of interior <code>shells</code> fully within the exterior <code>Shell</code>
that describe voids. Interior <code>shells</code> can not intersect each other and cannot contain another interior
<code>Shells</code>. A <code>Polyhedron</code> is a solid where each <code>Shell</code> is a set of <code>faces</code>
(MultiPolygons) and is closed, "watertight". The <code>Shell</code> splits space into two distinct regions, inside and 
outside the <code>Shell</code>. A <code>Polyhedron</code> is simple, i.e., <code>Faces</code> contained in a 
<code>Shell</code> do not intersect, rather they touch along common boundaries.

The JSON representation of a <code>Polyhedron</code> is a non-empty array of <code>MultiPolygon</code> arrays. Each
<code>MultiPolygon</code> array is a <code>Shell</code>. The first <code>Shell</code> is the exterior boundary, all 
other <code>Shells</code> are voids.

#### Relevance of Polyhedron to the 3D CSDM

It is assumed that a Boundary Representation [[5]](#5) is the logical approach to the definition of 3D cadastral parcels. 
ISO 19107:2019 [[6]](#6) includes Boundary Representation (B-Rep) for the geometric description of 3D vector data. The 
skin of a B-Rep is composed of a set of adjacent bounded elements called faces; cadastral boundary faces in this context, 
which defines the object’s Shell. Faces are bounded by a set of edges, or boundary lines, which are curves lying on the 
surfaces of the faces intersecting the edges. The points where several faces meet are called vertices and, in the 
cadastral realm, represent survey points generally. When physical markers are placed on the ground as part of a 
cadastral survey, they represent Boundary Marks. 

The data structure can be divided into two primary groups: one responsible for defining the object’s 
structure (the topology) and the other the form or shape of the object (the geometry). 

Within the 3D cadastral space, some cadastral parcels can be non-convex, so it is necessary to consider Polyhedron 
geometries with and without voids. Primarily, because in practice they are explicitly connected by faces that are common 
to the solid and the void - at least when adopting a B-Rep approach for geometry. The most common example in the 
cadastral space is the apartment block/building. For simplicity, say the external face of the building is represented by 
a 6 sided polyhedron, where the walls, floors, corridors, stairwells, etc., are all held under common ownership by the 
unit owners. The individual units, held in private ownership, are voids in the building unit – conceptually, little six 
sided polyhedra. It's also possible that the parent parcel that the building sits within is owned by a third party. If 
that was represented as a 3D cadastral parcel, then the building polyhedron would create a void in the parent parcel 
polyhedron. The basis of this construction is that in a cadastre, where Fee Simple ownership is considered to be unique, 
there can be no overlapping rights. An extension of the 2D no gaps, no overlaps topological rules. Other examples occur 
when there are tunnels passing through properties held by different owners.

As noted above, the GeoJSON-FG specification for a <code>Polyhedron</code> requires that unique <code>Polyhedron</code> 
do not intersect. From the perspective of a Cadastre, this suggests that if two 3D cadastral parcels intersect (Parcel A 
and Parcel B in the [Figure 1](#fig_1) below), say a height-limited Fee Simple Parcel (Parcel A) and an Easement Parcel (Parcel B), 
then the two parcels must be split into parts defined by those parts that are common to both parcels - the 
**Intersection** (Parcel A &cap; Parcel B) of the parcels (Part 2 in [Figure 1](#fig_1)), and those parts of the parcels that do not 
intersect (Parts 1 (Parcel A - Parcel B) and 3 (Parcel B - Parcel A)). 

The Parcels are then aggregated as two <code>MultiPolyhedron</code>. Parcel A equals Part 1 plus Part 2, and Parcel B 
equals Part 2 plus Part 3.

<a id="fig_1">![Figure 1: B-REP Partition of two intersecting Solids](images%2Fg77318.png "Figure 1: B-REP Partition of 
two intersecting Solids")</a>

As depicted in [Figure 2](#fig_2) an alternative and arguably simpler approach, as outline during the development of the 
[ICSM Conceptual Model for 3D CSDM](https://icsm-au.github.io/3d-csdm-design/2022/spec.html), is to not split 3D parcels into parts as described above, but define an 
**intersection curve** [[7]](#7) that describes where two solids meet explicitly.

<a id="fig_2">![Intersection of Solids defined by an Intersection Curve](images%2Fg14043.png "Intersection of Solids 
defined by an Intersection Curve")</a>

### MultiPolyhedron

A <code>MultiPolyhedron</code> is a collection of <code>Polyhedron</code> geometries with no assumptions regarding 
topological relationships between the <code>Polyhedron</code> objects. Generally <code>Polyhedron</code> objects 
contained in a <code>MultiPolyhedron</code> will not intersect each other.

In accordance with ISO 19107:2019 [[6]](#6) the geometry of a <code>MultiPolyhedron</code> is the union of all 
<code>Polyhedron</code> objects, so if objects do overlap the volume of the <code>MultiPolyhedron</code> will be less 
than the sum of the <code>Polyhedron</code> objects.

The collection of <code>Polyhedron</code> objects is represented as a JSON array. The order of the 
<code>Polyhedron</code> objects in the array is not significant.

#### Relevance of MultiPolyhedron to the 3D CSDM

Within the cadastral space it is quite common for an ownership title to consist of more than one cadastral parcel. Both 
composite (two or more contiguous parcels) and aggregate (two or more non-contiguous parcels) collections of polyhedra 
may be required. An **Estate** Parcel is defined as *the spatial extent of an Estate, which may consist of one or more 
cadastral parcels*. As such, while there is limited (no known) existing implementations for <code>Polyhedron</code> 
specifications using a <code>MultiPolygon</code> array, this construction appears to be appropriate for cadastral 
implementations.

### Prism

JSON-FG [[2]](#2) describes a <code>Prism</code> as a 3D geometry defined by a base shape (e.g., Polygon or Circle) that 
is then extruded from some optional lower limit to an upper limit. The limits are measured relative to a specified 3D 
CRS. If the base geometry is a <code>Point</code> the extrusion is a line extending from the lower limit to an upper 
limit. If the base geometry is a <code>Curve</code> the extrusion is a <code>Surface</code> extending from the lower 
limit to an upper limit. If the base geometry is a <code>Face</code> the extrusion is a solid whose footprint takes the 
same shape as the base geometry and extends from the lower limit to the upper limit.

More generally a <code>Prism</code> as describe falls under swept geometries, which are not covered by ISO 19107
[[6]](#6). However, IFC for example, does include swept geometries. Swept geometry methods are also included in many CAD 
applications. 

#### Relevance of Prism to the 3D CSDM

Many cadastral parcels in a 2D cadastre have vertical limits. They have been described as a Polygonal Slice [[8]](#8). 
There are also numerous examples in the mining industry where mining rights extend from ground level to some depth below 
ground. 

Easements are sometimes defined by a centre-line and easement offsets either side of the centre-line. Tunnels can 
be defined by a 3D centre-line and a geometry describing the cross-section of the tunnel. All are examples of swept 
geometries generally. Many 3D cadastral parcels can clearly be represented using a <code>Prism</code> geometry. 

Most conventional 2D cadastral parcels require a non-2-manifold geometry (unbounded volumes), as they are unbounded in 
the Z-axis. ISO 19152 [[9]](#9) refers to these representations as Liminal Spatial Units and represents them using a 2D boundary 
face string (on the map datum) and vertical boundary faces. In effect, fake edges are required at some arbitrary 
elevation to allow various spatial operations to be performed, for example, it is not possible to determine the 
orientation of a face extending to &plusmn; &infin; in the Z axis.

As such, the ability to specify a <code>Prism</code> geometry, or more generally a <code>SweptPath</code> geometry is of 
value to a cadastral system.

In terms of the [ICSM Conceptual Model for 3D CSDM](https://icsm-au.github.io/3d-csdm-design/2022/spec.html) the JSON-FG
Prism geometry is defined as an extrusion or Extruded Geometry, being a *3D geometry generated by 
extending a 2D geometry (the base) along a specified path or axis.*

### MultiPrism

A <code>MultiPrism</code> is an array of prism objects. The order of the prism geometry objects in the array is not 
significant.

#### Relevance of MultiPrism to the 3D CSDM

As with [MultiPolyhedron](#relevance-of-multipolyhedron-to-the-3d-csdm) it is anticipated that collections of 
<code>Prism</code> geometries will be encounterd in a 3D cadastre. For example multiple tunnels making up an underground 
network.


## Draft 3D Geometry Examples

The following sections describe the geometries proposed for inclusion in a 3D CSDM implementation. 3D geometry 
construction follows the same topological pattern described for 2D geometries. As such, it is only necessary to specify
a single set of patterns for each of the GeoJSON-FG geometries described above. Each geometry contains a 
<code>topology</code> element that references a set of lower order geometry IDs that as a set describe the higher level 
geometry: for example a set of <code>LineStrings</code> describe a <code>Polygon</code>; a set of <code>Polygons</code>
define the exterior of a <code>Solid</code>, etc.  For simplicity JSON-FG geometry types labels have been adopted where
appropriate.

Because observed vectors may be measured in any direction it is expected that a parser will check orientation and 
closure of geometries to ensure that they are well-formed.

### Points

Following ISO 19107's topological approach to the definition of geometries, and
[OGC's JSON-FG](https://docs.ogc.org/per/21-017r1.html) information encoding, 3D <code>Point</code> geometries are defined
by a <code>place</code> element that contains an <code>id</code> element to uniquely identify the <code>Point</code>, a
<code>type</code> element specifying the type of geometry being defined, and a <code>coordinate</code> triple (X, Y, Z) 
as follows:

~~~json lines
{
  "id": "123456",
  "place": {
    "type": "Point",
    "coordinates": [
      794317.443,
      398759.23,
      100.00
    ]
  }
}
~~~

The horizontal coordinate values are with respect to the horizontal Coordinate Reference System (CRS) defined by the 
CSD's horizontal CRS element. The vertical coordinate is with respect to the vertical datum defined by the CSD's 
vertical CRS element. A compound CRS may be substituted for horizontal and vertical CRS.

### Curves and Polygons

3D Curves and Polygons are specified in the same way that 2D [Curves](../../3d-csdm-data/Test%20Cases/csdm_2d_geometires.md#curves) and 
[Polygons](../../3d-csdm-data/Test%20Cases/csdm_2d_geometires.md#polygons) are with the restriction that 3D <code>Curves</code> must be constructed using 
3D <code>Points</code>. Parsers must be able to interprete <code>LineString</code>, <code>Arc</code>, 
<code>ArcWithCentre</code>, <code>CubicSpline</code>, etc. when constructing <code>Polygons</code> in 3D. 

If a 3D <code>Polygon</code> is not planar it may be beneficial for the data creator to define the surface form of a 
<code>Polygon</code>. Although this is not considered necessary from a data transport perspective as surface form is 
considered to be primarily a visualisation question. 

It is anticipated that most <code>Solid</code> <code>Faces</code> 
will be planar. But many may not, particularly when the exterior ring of a <code>Face</code> includes non-linear 
<code>Curves</code>. Given the nature of cadastral parcels, it is assumed that the surface of a <code>Solid</code> will
exhibit geometric seams along <code>Face</code> edges, i.e., the surface of the solid will not be smooth and continuous. 
Tessellation of a <code>Face</code> into triangles, parametric surface representation, or surface interpolation are 
common methods used to compute the surface of a <code>Face</code>.

For the specification of a <code>Curve</code> defined as a <code>LineString</code> the <code>topology</code> element 
references two 3D <code>Points</code>.

~~~json lines
{
  "id": "234561",
  "topology": {
    "type": "LineString",
    "references": [
      "1746055",
      "1746030"
    ]
  }
}
~~~
For the specification of a <code>Face</code> defined as a <code>Polygon</code> the <code>topology</code> element 
references at least three <code>Curves</code>. The <code>references</code> element is an array of arrays, where the 
first array of IDs defines the exterior of the <code>Face</code> and any subsequent arrays of IDs define voids in the 
<code>Face</code>. The next example is a <code>Face</code> that contains no voids.
~~~json lines
{
  "id": "2345671",
  "topology": {
    "type": "Polygon",
    "references": [
      [
        "234567",
        "234568",
        "234569",
        "234570"
      ]
    ]
  }
}
~~~

A <code>Face</code> with a void.

~~~json lines
{
   "id": "2345671",
   "topology": {
      "type": "Polygon",
      "references": [
         [
            "234567",
            "234568",
            "234569",
            "234570"
         ],
         [
            "334567",
            "334568",
            "334569",
            "334570"
         ]
      ]
   }
}
~~~

### Polyhedron

A <code>Solid</code> defined as a <code>Polyhedron</code> geometry type contains a <code>topology</code> element that 
contains an array of arrays. The first array references a set of <code>Face</code> IDs that define the exterior of the 
<code>Solid</code>. Interior surfaces  of voids are described in subsequent arrays. The <code>Face</code> IDs can be any <code>Polygon</code> that conforms 
to the 3D CSDM specification for a <code>Polygon</code>.  For a <code>Polyhedron</code> solid to be 
well-formed, the orientation of each <code>Face</code> of the polyhedron is such that the upwards Normal of each 
<code>Face</code> is outwards, and the <code>Polyhedron</code> is closed.

It is anticipated that a parser will include functionality to determine if a <code>Polyhedron</code> is closed and 
well-formed.

The next example is a <code>Polyhedron</code> that contains no voids.

~~~json lines
{
  "id": "3456712",
  "topology": {
    "type": "Polyhedron",
    "references": [
      [
        "234567",
        "234568",
        "234569",
        "234570"
      ]
    ]
  }
}
~~~

An example of a <code>Polyhedron</code> with a void.

~~~json lines
{
  "id": "3456712",
  "topology": {
    "type": "Polyhedron",
    "references": [
      [
        "234567",
        "234568",
        "234569",
        "234570"
      ],
      [
        "734567",
        "734568",
        "734569",
        "734570"
      ]
    ]
  }
}
~~~

### MultiPolyhedron

A <code>MultiPolyhedron</code> is a geometry collection of <code>Polyhedron</code> that contains a <code>topology</code> 
element that references an unordered array of <code>Polyhedron</code> IDs.

~~~json lines
{
   "id": "4456712",
   "topology": {
      "type": "MultiPolyhedron",
      "references": [
         "434567",
         "434568",
         "434569",
         "434570"
      ]
   }
}
~~~

### Prism
A <code>Solid</code> defined as a type of <code>Prism</code> contains a <code>topology</code> element that references a 
base geometry which could be <code>Point</code>, <code>Curve</code>, or <code>Polygon</code> geometry along with 
<code>lower</code> and <code>upper</code> elements. Together, these elements define the shape and vertical limits of the 
<code>Prism</code> extrusion. <code>Base</code>, <code>Lower</code>, and <code>Upper</code>are all required elements.

~~~json lines
{
  "id": "5456712",
  "topology": {
    "type": "Prism",
    "base": {
      "references": [
        "434567"
      ],
    },
    "lower": -10.00,
    "upper": 10.00
  }
}
~~~

### MultiPrism

A <code>MultiPrism</code> is a geometry collection of <code>Prisms</code> that contain a <code>topology</code> 
element that references an unordered array of <code>Prism</code> or <code>SweptPath</code> IDs.

~~~json lines
{
   "id": "6456712",
   "topology": {
      "type": "MultiPrism",
      "references": [
         "434567",
         "434568",
         "434569",
         "434570"
      ]
   }
}
~~~

### SweptPath
A <code>Solid</code> defined as a type of <code>SweptPath</code> contains a <code>topology</code> element that consists
of three elements, <code>base</code>, <code>origin</code>, and <code>path</code>. The <code>base</code>  is a 2D shape 
that is to be extruded into a <code>Solid</code>. The <code>base</code> geometry could be <code>Point</code>, 
<code>Curve</code>, or <code>Polygon</code> geometry.The <code>path</code> is the trajectory or direction along which 
the <code>base</code> geometry is extruded to create the 3D <code>Solid</code>. The path defines how the 
<code>base</code> geometry is extended in space. The <code>path</code> can be linear, curved, or follow any other 
specified trajectory. The <code>origin</code> geometry must be a <code>Point</code>. It defines the relationship between 
the <code>base</code> and the <code>path</code>. It could be a vertex of the <code>base</code>, the geometric centre of 
the <code>base</code> geometry, or some other location relative to the <code>base</code>.  The extrusion process involves 
taking the <code>base</code> geometry and moving it along the <code>path</code> geometry with respect to the 
<code>origin</code> to create a <code>Solid</code>, a new <code>Curve</code>, or <code>surface</code> in 3D. As the base 
shape moves along the <code>path</code>, it generates a new geometry, forming the extruded <code>Solid</code>.

When computing the <code>Shell</code> of the <code>SweptPath</code> it is assumed that the <code>base</code> geometry is 
perpendicular to the <code>path</code> and that the <code>origin</code> is dragged along the <code>path</code>.
As such a parser will require functionality to rotate the <code>base</code> geometry if the <code>base</code> geometry is 
not perpendicular to the <code>path</code> or the <code>path</code> is non-linear.

<code>Base</code>, <code>origin</code>, and <code>path</code> are required elements.

~~~json lines
{
   "id": "5456712",
   "topology": {
      "type": "SweptPath",
      "base": {
         "references": [
            "434567"
         ],
      },
      "origin": {
         "references": [
            "9374629"
         ],
      },
      "path": {
         "references": [
            "434567"
         ],
      }
   }
}
~~~

## 3D Geometry Operators 

In order to ensure that a valid set of geometries is contained in a 3D CSDM it is anticipated that a minimal set of 
functions will be required. It is expected that the set of functions will at least include the following:
1. Test to ensure <code>face</code> normal is outwards;
2. Test to ensure that <code>Solid</code> is well-formed and closed;
3. Test for intersection of geometries;
4. Function to compute non-planar <code>Face</code> surface;
5. Function to compute Surface-Surface intersection;
6. Function to construct Intersection Curve from two or more geometries that intersect;
7. Test that Intersection Curve closes.
8. If adopting a strict B-Rep approach, functions to split geometries that intersect and rebuild geometries from parts;
9. Functionality to rotate <code>base</code> geometry so that it is perpendicular to the <code>path</code> geometry.

## Definitions

| Term                  | Definition                                                                                                                                                                                                                       | Source                   |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| point                 | 0‑dimensional geometric primitive, representing a position.                                                                                                                                                                      | ISO 19136-1:2020, 3.1.47 |
| curve                 | A 1-dimensional geometric primitive. The boundary of a curve is the set of points at either end of the curve.                                                                                                                    | ISO 19136-1:2020, 3.1.17 |
| line string           | A curve composed of straight-line segments.                                                                                                                                                                                      | ISO 19136-1:2020, 3.1.40 |
| surface               | Geometric surface in some Euclidean space, usually &#8477;&sup3;, that represents an approximation to the surface of the Earth possibly restricted to a small area but often covering the entire globe.                          | ISO 19107:2019, 3.52     |
| Polygon               | Planar surface defined by an exterior boundary and zero or more interior boundaries.                                                                                                                                             | ISO 19136-1:2020, 3.1.48 |
| node                  | 0‑dimensional topological primitive.                                                                                                                                                                                             | ISO 19107:2019,3.69      |
| edge                  | 1-dimensional topological primitive. The geometric realization of an edge is a curve. The boundary of an edge is the set of one or two nodes associated with the edge.                                                           | ISO 19107:2019, 3.29     |
| face                  | 2-dimensional topological primitive. The geometric realization of a face is a surface. The boundary of a face is the set of directed edges that are associated with the face via the boundary relations. These can be organized as rings. | ISO 19107:2019,3.38      |
| solid                 | 3-dimensional topological primitive. The boundary of a topological solid consists of a set of directed faces.                                                                                                                    | ISO 19107:2019, 3.101    |
| intersection curve    | A curve representing the boundary or contour where the surfaces of two solids meet or intersect. It is the set of points where points on the surface of one solid coincide with points on the surface of a second solid.         | [[7]](#7)                |
| topological primitive | topological object that represents a single, homogeneous, non-decomposable element                                                                                                                                               | ISO 19107:2019, 3.100    |
| geometric primitive   | geometric object representing a single, connected, homogeneous (isotropic) element of space.                                                                                                                                     | ISO 19107:2019, 3.50     |



## References
<a id="1">[1]</a> 
Butler, H., Daly, M., Doyle, A., Gillies, S., Hagen, S., & Schaub, T. (2016). GeoJSON (7946). https://datatracker.ietf.org/doc/html/rfc7946

<a id="2">[2]</a> 
Open Geospatial Consortium. 2023. OGC Features and Geometries JSON - Part 1: Core. https://docs.ogc.org/DRAFTS/21-045.html

<a id="3">[3]</a> 
ISO. ISO/IEC 13249-3:2016 Information technology — Database languages — SQL multimedia and application packages — Part 3: Spatial

<a id="4">[4]</a> 
The PostGIS Development Group. 2023. PostGIS 3.4.2dev Manual. https://postgis.net/docs/index.html

<a id="5">[5]</a>
Stroud, I. (2006). Boundary Representation Modelling Techniques. Springer.

<a id="6">[6]</a>
ISO. ISO 19107:2019. Geographic information — Spatial schema. https://www.iso.org/obp/ui/#iso:std:iso:19107:ed-2:v1:en

<a id="7">[7]</a>
Barnhill, R. E., Farin, G., Jordan, M., & Piper, B. R. (1987). Surface/surface intersection. Computer Aided Geometric Design, 4(1), 3–16. https://doi.org/10.1016/0167-8396(87)90020-3

<a id="8">[8]</a>
Thompson, R., Van Oosterom, P., Karki, S., & Cowie, Ben. (2015). A Taxonomy of Spatial Units in a Mixed 2D and 3D Cadastral Database. From the Wisdom of the Ages to the Challenges of the Modern World. FIG Working Week 2015, Sofia, Bulgaria.

<a id="9">[9]</a>
ISO. ISO 19152:2012 Land Administration Domain Model (LADM). https://www.iso.org/obp/ui/#iso:std:iso:19152:ed-1:v1:en.

