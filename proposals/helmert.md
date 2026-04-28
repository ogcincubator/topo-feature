# Helmert Transformation

A Helmert transformation is a similarity transformation. 
It preserves shape as a common scale factor is applied.
This is an important consideration for Cadastral and BIM data where it is important that local shape is maintained when the data is transformed..
When applying a 3D translation, a rotation about the Z axis and a common scale factor a 4 x 4 matrix can be applied to solve the transformation.

## Basic transformation model

Let the source / local coordinate be:

$$ p =\begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}$$

and the transformed / map coordinate be:

$$P = \begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix}$$

Then:

$$P = T R_z S p$$

where:

$S$ is the common scale factor matrix

$R_z$ is the rotation matrix about the Z axis

$T$ is the translation matrix

Applied in this order, the local coordinates are first scaled, then rotated, then translated.

## Common Scale Matrix

If the common scale factor is $s$, then:
$$S = \begin{bmatrix} s & 0 & 0 & 0 \\ 0 & s & 0 & 0 \\ 0 & 0 & s & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

If `s = 1.0000` there is no scaling. Many map projections have a central meridian scale factor `s = 0.99996` which will reduce the local coordiates slightly.
Note that it is the combined Scale Factor at the target location that should generally be applied. 
The combined scale factor is the product of the Grid Scale Factor and the Elevation Scale Factor.

Other common scales are:

- `s = 0.0254` for inches to meters
- `s = 0.3048` for feet to meters
- `s = 0.201168` for links to meters

## Z-Rotation Matrix

For a right-handed coordinate system, with positive rotation counter-clockwise in the XY plane:

$$R_z = \begin{bmatrix} \cos(\theta) & -\sin(\theta) & 0 & 0 \\ \sin(\theta) & \cos(\theta) & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

where $\theta$ is the rotation angle in radians.

## Translation Matrix

If the translation from the local system to the target/map system is `tx, ty, tz`, then:

$$T = \begin{bmatrix} 1 & 0 & 0 & tx \\ 0 & 1 & 0 & ty \\ 0 & 0 & 1 & tz \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

## Combined Transformation Matrix

Because the scale is common, the scale and rotation can be combined directly:

$$M = \begin{bmatrix} s\cos(\theta) & -s\sin(\theta) & 0 & t_x \\ s\sin(\theta) & s\cos(\theta) & 0 & t_y \\ 0 & 0 & s & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

then:

$$\begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix} = \begin{bmatrix} s\cos(\theta) & -s\sin(\theta) & 0 & t_x \\ s\sin(\theta) & s\cos(\theta) & 0 & t_y \\ 0 & 0 & s & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}$$

Expanded into equations:

$$\begin{aligned}
X &= t_x + s(x\cos\theta - y\sin\theta) \\
Y &= t_y + s(x\sin\theta + y\cos\theta) \\
Z &= t_z + sz \\
\end{aligned}$$

## Example

Assuming the local origin is `0, 0, 0`, and the target system is at `392000.0, 6465000.0, 12.4`, with a scale factor of `1.0` and rotation angle of `34.46031` degrees

then:

$\theta = 34.46031\frac{\pi}{180}$

and: 

$$M=\begin{bmatrix} 0.8243 & -0.5662 & 0.0 & 392000.0 \\ 0.5662 & 0.8243 & 0.0 & 6465000.0 \\ 0.0 & 0.0 & 1.0 & 12.4 \\ 0.0 & 0.0 & 0.0 & 1.0 \end{bmatrix}$$

## Conventions

Rotations must be explicitly defined

```text
positive counter-clockwise from local X to target X
```
or
```text
clockwise from north / grid north
```

This matters because surveying, BIM, GIS, and graphics software do not always use the same sign conventions.

For the matrix algebra above, the convention is:

```text
right-handed coordinate system
X = east
Y = north
Z = up
positive θ = counter-clockwise rotation in the XY plane
transformation direction = local CRS to target CRS
matrix multiplication = column-vector convention
```
The convention should be stated anywhere that the matrix is encoded.

```json
{
  "operationMethod": "HelmertSimilarity3D_ZRotation",
  "transformationDirection": "source-to-target",
  "matrixConvention": "column-vector; target = M * source",
  "axisConvention": "right-handed; X east, Y north, Z up",
  "zAxisRotationConvention": "positive counter-clockwise from +X/east",
  "parameters": {
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
  "matrix": [
    [0.8243, -0.5662, 0.0, 392000.0],
    [0.5662,  0.8243, 0.0, 6465000.0],
    [0.0,     0.0,    1.0, 12.4],
    [0.0,     0.0,    0.0, 1.0]
  ]
}
```

The Helmert Transformation description is effectively a restricted Helmert / Similarity transformation suitable for many BIM or CAD datasets where the local model only needs a plan rotation, a common scale, and a translation into the jurisdictional CRS.

## Clockwise from North

If the angle is defined clockwise from north / grid north, the main change is that the angle is no longer the standard mathematical angle used by the usual rotation matrix.
The bearing-style angle must first be converted into a standard mathematical rotation angle before using the usual matrix.

Let:

$\alpha$ = clockwise angle from north / grid north

$\theta$ = standard mathematical angle from +X, positive counter-clockwise

Then:

$\theta = 90-\alpha$

or in radians:

$\theta = (90 - \alpha)\frac{\pi}{180}$

The specification of the rotation angle is:

```json
{
  "zAxisRotationConvention": "bearing of local +X axis; clockwise from grid north"
}
```

## Direct bearing-form matrix

You can also avoid the conversion and write the matrix directly in terms of the clockwise-from-north angle $\alpha$.

Since:

$\begin{aligned}\cos(90-\alpha) = \sin(\alpha) \\ \sin(90-\alpha) = \cos(\alpha)\end{aligned}$

the matrix becomes:

$$\begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix} = \begin{bmatrix} s\sin(\alpha) & -s\cos(\alpha) & 0 & t_x \\ s\cos(\alpha) & s\sin(\alpha) & 0 & t_y \\ 0 & 0 & s & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}$$

This direct matrix assumes that $\alpha$ is the bearing of the local +X axis measured clockwise from grid north.

## Common Alternative

Sometimes _clockwise from north_ is used to describe the bearing of the local +Y axis, not the local +X axis. 
In BIM/CAD this is common when people say the project “Y axis” is aligned with north or grid north.

In this case, let:

$\beta$ = bearing of local +Y measured clockwise from north

Then the standard mathematical rotation angle is:

$\theta = -\beta$

and the matrix is:
$$\begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix} = \begin{bmatrix} s\cos(\beta) & s\sin(\beta) & 0 & t_x \\ -s\sin(\beta) & s\cos(\beta) & 0 & t_y \\ 0 & 0 & s & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix}$$

If $\beta=0$ the local +Y axis is aligned with North, so no rotation needs to be applied.

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

## References

Robinson, A.H., J.L. Morrison, P.C. Muehrcke, A.J. Kimerling, and S.C. Guptill. 1995. Elements of Cartography. 6th edn Hoboken, NJ: John Wiley & Sons.

Snyder, J.P. 1987. Map Projections–a Working Manual. USGPO. http://pubs.er.usgs.gov/publication/pp1395.

Wolf, Paul R., Bon DeWitt, and Benjamin Wilkinson. 2014. Elements of Photogrammetry with Application in GIS. 4th edn London, UK: McGraw-Hill.

