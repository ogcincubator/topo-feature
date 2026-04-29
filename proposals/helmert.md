# Helmert / Similarity Transformation

A Helmert transformation is a similarity transformation.
It applies translation, rotation, and one common scale factor.
Because the same scale factor is applied to all axes, the transformation preserves shape.

For 3D CSDM tool-support purposes, a Helmert or similarity transformation should be described as a **coordinate operation** between a **source CRS** and a **target CRS**.

In the local CRS use case:

- the **source CRS** will commonly be a local or Engineering CRS used by a BIM, CAD, engineering, construction, or project-local dataset;
- the **target CRS** will normally be the jurisdictional or recognised CRS used to visualise or compare the supporting data with 3D CSDM content; and
- the **coordinate operation** describes how coordinates are transformed from the source CRS to the target CRS.

The matrix described below is therefore the **implementation form** of the coordinate operation.  
It does not define the CRS by itself.

## Ontology Alignment

To align with the OGC CRS Ontology pattern, the transformation should distinguish between:

1. the **source CRS**;
2. the **target CRS**;
3. the **coordinate operation**;
4. the **operation method**;
5. the **operation parameters**; and
6. the **implementation encoding**, such as a 4 $\times$ 4 matrix, [WKT2:2019](https://docs.ogc.org/is/18-010r7/18-010r7.html), or [PROJJSON](https://proj.org/en/stable/specifications/projjson.html).

In this case, the coordinate operation may be described as a restricted Helmert / similarity transformation where the operation parameters are:

```text
translation in X, Y, Z
rotation about the Z axis
one common scale factor
```

For a full 3D Helmert transformation, rotations about X, Y, and Z may be included.
However, for many BIM, CAD, and local-grid visualisation cases, a restricted form using Z-axis rotation is sufficient.

The matrix should be accompanied by explicit metadata describing:

```text
source CRS
target CRS
operation method
operation parameters
transformation direction
axis convention
rotation convention
scale convention
linear and angular units
vertical reference, where relevant
```

## Basic transformation model

Let the source / local coordinate be:

$$
p =
\begin{bmatrix}
x \\
y \\
z \\
1
\end{bmatrix}
$$

and the transformed / map coordinate be:

$$
P =
\begin{bmatrix}
X \\
Y \\
Z \\
1
\end{bmatrix}
$$

Then:

$$P = T R_z S p$$

where:

- $S$ is the common scale factor matrix;
- $R_z$ is the rotation matrix about the $Z$ axis; and
- $T$ is the translation matrix.

Applied in this order, the local coordinates are first scaled, then rotated, then translated.

This assumes the following matrix convention:

```text
column-vector convention
target = M * source
transformation direction = source CRS to target CRS
```

## Common Scale Matrix

If the common scale factor is $S$, then:
$$
S =
\begin{bmatrix}
s & 0 & 0 & 0 \\
0 & s & 0 & 0 \\
0 & 0 & s & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

If `s = 1.0000` there is no scaling.

Many map projections have a grid scale factor that slightly changes the relationship between ground distances and grid distances.
Where scale is required, it is generally the combined scale factor at the target location that should be applied.

The combined scale factor is the product of:

```text
grid scale factor x elevation scale factor.
```
Other common scales are:

- `s = 0.0254` for inches to meters
- `s = 0.3048` for feet to meters
- `s = 0.201168` for links to meters

## Z-Rotation Matrix

For a right-handed coordinate system, with positive rotation counter-clockwise in the XY plane:

$$
R_z =
\begin{bmatrix}
\cos(\theta) & -\sin(\theta) & 0 & 0 \\
\sin(\theta) & \cos(\theta)  & 0 & 0 \\
0            & 0             & 1 & 0 \\
0            & 0             & 0 & 1
\end{bmatrix}
$$

where $\theta$ is the rotation angle in radians.

If the rotation angle is provided in degrees:

$$\theta = \frac{\theta_{deg}}{180}\pi$$

## Translation Matrix

If the translation from the source / local CRS to the target CRS is $t_x$, $t_y$, and $t_z$, then:

$$
T =
\begin{bmatrix}
1 & 0 & 0 & t_x \\
0 & 1 & 0 & t_y \\
0 & 0 & 1 & t_z \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

## Combined Transformation Matrix

Because the scale is common, the scale and rotation can be combined directly:

$$
M =
\begin{bmatrix}
s\cos(\theta) & -s\sin(\theta) & 0 & t_x \\
s\sin(\theta) &  s\cos(\theta) & 0 & t_y \\
0             & 0              & s & t_z \\
0             & 0              & 0 & 1
\end{bmatrix}
$$

then:

$$
\begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix}
=
\begin{bmatrix}
s\cos(\theta) & -s\sin(\theta) & 0 & t_x \\
s\sin(\theta) &  s\cos(\theta) & 0 & t_y \\
0             & 0              & s & t_z \\
0             & 0              & 0 & 1
\end{bmatrix}
\begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}
$$

Expanded into equations:

$$\begin{aligned}
X &= t_x + s(x\cos\theta - y\sin\theta) \\
Y &= t_y + s(x\sin\theta + y\cos\theta) \\
Z &= t_z + sz \\
\end{aligned}$$

## Example

Assume:

```text
source CRS = local Engineering CRS
target CRS = GDA2020 / MGA zone 50
local origin = 0, 0, 0
target origin = 392000.0, 6465000.0, 12.4
scale factor = 1.0
rotation about Z = 34.46031 degrees
```

then:

$\theta = 34.46031\frac{\pi}{180}$

Using approximate values:

```text
cos(34.46031°) ≈ 0.8243
sin(34.46031°) ≈ 0.5662
```

the matrix is: 

$$
M =
\begin{bmatrix}
0.8243 & -0.5662 & 0.0 & 392000.0  \\
0.5662 &  0.8243 & 0.0 & 6465000.0 \\
0.0    &  0.0    & 1.0 & 12.4      \\
0.0    &  0.0    & 0.0 & 1.0
\end{bmatrix}
$$

## Required Operation Conventions

Rotations must be explicitly defined.

For example:

```text
positive counter-clockwise from +X / east
```

or:

```text
clockwise from north / grid north
```

This matters because surveying, BIM, GIS, CAD, and graphics software do not always use the same sign conventions.

For the matrix algebra above, the convention is:

```text
source CRS = local Engineering CRS
target CRS = jurisdictional or recognised CRS
right-handed coordinate system
X = east
Y = north
Z = up
positive θ = counter-clockwise rotation in the XY plane
transformation direction = source CRS to target CRS
matrix multiplication = column-vector convention
target = M * source
```
These conventions should be encoded as metadata associated with the coordinate operation.

## Example Operation Encoding

The following JSON-LD-style example shows how the transformation can be described as a coordinate operation.
The matrix is included as the executable implementation form.

```json
{
  "@context": {
    "geosrs": "https://w3id.org/geosrs/",
    "srs": "https://w3id.org/geosrs/srs/",
    "co": "https://w3id.org/geosrs/co/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "csdm-crs": "https://example.org/3d-csdm/crs-support/"
  },
  "@id": "csdm-crs:operation/local-to-map",
  "@type": "co:CoordinateOperation",
  "rdfs:label": "Building A local engineering CRS to GDA2020 / MGA zone 50",
  "co:sourceCRS": "csdm-crs:crs/local-building-a",
  "co:targetCRS": "http://www.opengis.net/def/crs/EPSG/0/7850",
  "operationMethod": "Restricted Helmert / similarity transformation",
  "operationParameters": {
    "translation": {
      "tx": 392000.0,
      "ty": 6465000.0,
      "tz": 12.4,
      "unit": "metre"
    },
    "rotation": {
      "zAxisDegrees": 34.46031,
      "unit": "degree"
    },
    "scale": {
      "value": 1.0,
      "unit": "unity"
    }
  },
  "operationConventions": {
    "transformationDirection": "source-to-target",
    "matrixConvention": "column-vector; target = M * source",
    "axisConvention": "right-handed; X east, Y north, Z up",
    "zAxisRotationConvention": "positive counter-clockwise from +X/east"
  },
  "implementationMatrix": [
    [0.8243, -0.5662, 0.0, 392000.0],
    [0.5662,  0.8243, 0.0, 6465000.0],
    [0.0,     0.0,    1.0, 12.4],
    [0.0,     0.0,    0.0, 1.0]
  ],
  "operationEncoding": {
    "format": "PROJJSON",
    "definition": {}
  }
}
```

The `implementationMatrix` allows software to execute the transformation directly.
The CRS and coordinate-operation metadata explain what the matrix means.

Where ontology-crs terms are available, they should be used to describe the CRS and coordinate operation resources.
Where implementation-specific details are required, such as a homogeneous transformation matrix or matrix multiplication convention, the 3D CSDM tool-support profile may define additional properties.

## Clockwise from North

If the angle is defined clockwise from north / grid north, the main change is that the angle is no longer the standard mathematical angle used by the usual rotation matrix.

The standard matrix assumes:

```text
0° is along +X / east
positive rotation is counter-clockwise
```

A bearing or azimuth convention assumes:

```text
0° is along +Y / north
positive rotation is clockwise
```

Therefore, the bearing-style angle must first be converted into a standard mathematical rotation angle before using the usual matrix.

Let:

$\alpha$ = clockwise angle from north / grid north

and:

$\theta$ = standard mathematical angle from $+X$, positive counter-clockwise

Then:

$\theta = 90-\alpha$

or in radians:

$\theta = (90 - \alpha)\frac{\pi}{180}$

The specification of the rotation angle should make the convention explicit:

```json
{
  "zAxisRotationConvention": "bearing of local +X axis; clockwise from grid north"
}
```

## Direct bearing-form matrix

The conversion can also be avoided by writing the matrix directly in terms of the clockwise-from-north angle $\alpha$.

Since:

$\begin{aligned}\cos(90-\alpha) = \sin(\alpha) \\ \sin(90-\alpha) = \cos(\alpha)\end{aligned}$

the matrix becomes:

$$
\begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix}
=
\begin{bmatrix}
s\sin(\alpha) & -s\cos(\alpha) & 0 & t_x \\
s\cos(\alpha) &  s\sin(\alpha) & 0 & t_y \\
0             & 0              & s & t_z \\
0             & 0              & 0 & 1
\end{bmatrix}
\begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}
$$

This direct matrix assumes that $\alpha$ is the bearing of the local $+X$ axis measured clockwise from grid north.

## Common Alternative: Bearing of Local $+Y$ Axis

Sometimes _clockwise from north_ is used to describe the bearing of the local $+Y$ axis, not the local $+X$ axis. 
In BIM/CAD this is common when people say the project “Y axis” is aligned with north or grid north.

In this case, let:

$\beta$ = bearing of local $+Y$ axis measured clockwise from north

Then the standard mathematical rotation angle is:

$\theta = -\beta$

and the matrix is:

$$
\begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix}
=
\begin{bmatrix}
 s\cos(\beta) & s\sin(\beta) & 0 & t_x \\
-s\sin(\beta) & s\cos(\beta) & 0 & t_y \\
0             & 0            & s & t_z \\
0             & 0            & 0 & 1
\end{bmatrix}
\begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}
$$

If $\beta=0$ the local $+Y$ axis is aligned with North, so no rotation needs to be applied.

The specification of the rotation angle is:

```json
{
  "zAxisRotationConvention": "bearing of local +Y axis; clockwise from grid north"
}
```

## Math if Rotations about the X- and Y-Axis are required - General 3D Helmert Transformation

The general 3D affine transformation matrix is:

$$
M =
\begin{bmatrix}
a_{11} & a_{12} & a_{13} & t_x \\
a_{21} & a_{22} & a_{23} & t_y \\
a_{31} & a_{32} & a_{33} & t_z \\
0      & 0      & 0      & 1
\end{bmatrix}
$$

then:

$$
\begin{bmatrix}
X \\
Y \\
Z \\
1
\end{bmatrix}
=
\begin{bmatrix}
a_{11} & a_{12} & a_{13} & t_x \\
a_{21} & a_{22} & a_{23} & t_y \\
a_{31} & a_{32} & a_{33} & t_z \\
0      & 0      & 0      & 1
\end{bmatrix}
\begin{bmatrix}
x \\
y \\
z \\
1
\end{bmatrix}
$$

Expanded into equations:

$$
\begin{aligned}
X &= a_{11}x + a_{12}y + a_{13}z + t_x \\
Y &= a_{21}x + a_{22}y + a_{23}z + t_y \\
Z &= a_{31}x + a_{32}y + a_{33}z + t_z
\end{aligned}
$$

The coefficients $a_{11}$ to $a_{33}$ define the combined effect of rotation and scale. The values $t_x$, $t_y$, and $t_z$ define the translation.

## Matrix from Translation, Rotation, and Axis Scale

Where the Helmert transformation is limited to translation, rotation, and common scale, the matrix can be constructed as:

$$
M = T R_z R_y R_x S
$$

where:

- $S$ is the common scale matrix described [above](#common-scale-matrix);
- $R_x$ is the rotation matrix about the X axis;
- $R_y$ is the rotation matrix about the Y axis;
- $R_z$ is the rotation matrix about the Z axis described [above](#z-rotation-matrix).; and
- $T$ is the translation matrix described [above](#translation-matrix).

Applied in this order, the local coordinates are first scaled, then rotated about $X$, then rotated about $Y$, then rotated about $Z$, then translated.

## X-Rotation Matrix

For a right-handed coordinate system, with positive rotation following the right-hand rule:

$$
R_x =
\begin{bmatrix}
1 & 0             & 0              & 0 \\
0 & \cos(\omega)  & -\sin(\omega)  & 0 \\
0 & \sin(\omega)  & \cos(\omega)   & 0 \\
0 & 0             & 0              & 1
\end{bmatrix}
$$

where $\omega$ is the rotation angle about the X axis.

## Y-Rotation Matrix

$$
R_y =
\begin{bmatrix}
\cos(\phi)   & 0 & \sin(\phi) & 0 \\
0            & 1 & 0          & 0 \\
-\sin(\phi)  & 0 & \cos(\phi) & 0 \\
0            & 0 & 0          & 1
\end{bmatrix}
$$

where $\phi$ is the rotation angle about the Y axis.

## $M$ as a 4 $\times$ 4 Matrix

Using the same column-vector convention described above:

```text
target = M * source
```
and assuming the transformation order is:

```text
scale first, then rotate about X, then Y, then Z, then translate
```

the combined Helmert matrix is:

$$
M = T R_z R_y R_x S
$$

where:

$T$: Translation matrix

$R_z$: Rotation about Z-axis

$R_y$: Rotation about Y-axis

$R_x$: Rotation about X-axis

$S$: Scaling matrix

Let:

$s$ = the common scale factor

$\omega$          = rotation about X

$\phi$          = rotation about Y

$\theta$        = rotation about Z

$t_x$, $t_y$, $t_z$ = translation

Using:

$c_\omega = \cos(\omega), s_\omega = \sin(\omega)$

$c_\phi = \cos(\phi), s_\phi = \sin(\phi)$

$c_\theta = \cos(\theta), s_\theta = \sin(\theta)$

The combined matrix is:

$$M =
\begin{bmatrix}
 s c_\theta c_\phi & s (c_\theta s_\phi s_\omega - s_\theta c_\omega) & s (c_\theta s_\phi c_\omega + s_\theta s_\omega) & tx \\
s s_\theta c_\phi & s (s_\theta s_\phi s_\omega + c_\theta c_\omega) & s (s_\theta s_\phi c_\omega - c_\theta s_\omega) & ty \\
-s s_\phi & s c_\phi s_\omega & s c_\phi c_\omega & tz \\
0 & 0 & 0 & 1
\end{bmatrix}$$

> **Note**:
> This matrix assumes:
> ```text
> right-handed coordinate system
> X = east
> Y = north
> Z = up
> positive rotations follow the right-hand rule
> rotation order = X, then Y, then Z
> scale order = before rotation
> transformation direction = source/local to target/map
> matrix convention = column-vector; target = M * source.
> ```
> Order matters: $M = T R_z R_y R_x S$ **is not the same as** $S R_x R_y R_z T$
> 
> So it is recommended that expected transformation order is declared in the metadata

### Suggested JSON Encoding

```json
{
  "operationMethod": "Helmert3D",
  "transformationDirection": "source-to-target",
  "matrixConvention": "column-vector; target = M * source",
  "axisConvention": "right-handed; X east, Y north, Z up",
  "rotationConvention": "positive rotations follow the right-hand rule",
  "rotationOrder": "X then Y then Z",
  "parameters": {
    "translation": {
      "tx": 392000.0,
      "ty": 6465000.0,
      "tz": 12.4,
      "unit": "metre"
    },
    "rotation": {
      "xAxisDegrees": 0.0,
      "yAxisDegrees": 0.0,
      "zAxisDegrees": 34.46031,
      "unit": "degree"
    },
    "scale": {
      "sx": 1.0,
      "sy": 1.0,
      "sz": 1.0,
      "unit": "unity"
    }
  },
  "matrix": [
    [0.8243, -0.5662, 0.0, 392000.0],
    [0.5662,  0.8243, 0.0, 6465000.0],
    [0.0,     0.0,    1.0, 12.4],
    [0.0,     0.0,    0.0, 1.0]
  ]
}
```

> **Note:** that if Scale is not constant, strictly, it is an Affine Transformation.
> But the only difference is that the $S$ matrix allows different values for elements $a_{11}$, $a_{22}$, and $a_{33}$.

## Summary

The Helmert transformation described here is a restricted Helmert / similarity transformation suitable for many BIM, CAD, or local-grid visualisation cases where the local model only needs:

```text
translation into the target CRS
plan rotation
one common scale factor
```

For 3D CSDM tool support, the transformation should be described as a coordinate operation from a source Engineering CRS to a target jurisdictional or recognised CRS.

The 4 $\times$ 4 matrix is the executable implementation form of that coordinate operation.
It should be accompanied by semantic CRS and coordinate-operation metadata so that software can understand:

```text
what CRS the source coordinates are in
what CRS the target coordinates are in
what operation is being applied
what parameters and units are used
what conventions are required to interpret the matrix
```
## References

buildingSMART International Limited. 2024. ‘IFC 4.3.2 Documentation’. https://ifc43-docs.standards.buildingsmart.org/ 

CRS Ontology Working Group Github. 2026. ‘Ontology-CRS’. https://github.com/opengeospatial/ontology-crs.

ISO, 2019. ‘ISO 19111:2019(En), Geographic Information — Referencing by Coordinates’. https://www.iso.org/obp/ui/en/#iso:std:iso:19111:ed-3:v1:en:en). (April 29, 2026).

Lott, Roger, ed. 2019. ‘Geographic Information — Well-Known Text Representation of Coordinate Reference Systems’. https://docs.ogc.org/is/18-010r7/18-010r7.html.

PROJ Contributors. 2026. ‘PROJJSON — PROJ 9.8.1 Documentation’. https://proj.org/en/stable/specifications/projjson.html

Robinson, A.H., J.L. Morrison, P.C. Muehrcke, A.J. Kimerling, and S.C. Guptill. 1995. Elements of Cartography. 6th edn Hoboken, NJ: John Wiley & Sons.

Snyder, J.P. 1987. Map Projections–a Working Manual. USGPO. http://pubs.er.usgs.gov/publication/pp1395.

Wolf, Paul R., Bon DeWitt, and Benjamin Wilkinson. 2014. Elements of Photogrammetry with Application in GIS. 4th edn London, UK: McGraw-Hill.


