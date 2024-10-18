# CityJSON -> topoFeature type mapping
# (note: Surface is used as an auxiliary type)
def toTopoGeometry: {
  "MultiSurface": "MultiPolygon",
  "CompositeSurface": "MultiPolygon",
  "Solid": "Polyhedron",
  "MultiSolid": "MultiPolyhedron",
  "CompositeSolid": "MultiPolyhedron",
} as $MAP | ($MAP[.] // .);

# CityJSON geometry array contents mapping
# (note: Surface is used as an auxiliary type)
def nextGeometry: {
  "MultiPolyhedron": "Polyhedron",
  "Polyhedron": "MultiPolygon",
  "MultiPolygon": "Polygon",
  "Polygon": "LineString"
} as $MAP | $MAP[.];

# Accepts object with "references" (to inner geometries or vertices), "type", and optional "id"
def processBoundaries: .type as $TYPE | .id as $ID | (.type | toTopoGeometry) as $TOPO_TYPE | ($TOPO_TYPE | nextGeometry) as $NEXT_TYPE | {
  "@type": "Feature",
  "@id": ($ID // empty),
  "geometry": null,
  "topology": {
    "type": $TOPO_TYPE,
    "references": (if (.type == "MultiPoint" or .type == "LineString") then (.references | map("#vertices-\(.)")) else (.references | to_entries | map({
        "type": $NEXT_TYPE,
        "id": (if $ID then "\($ID)_\(.key + 1)" else empty end),
        "references": .value
      } | processBoundaries)) end)
  },
  "properties": null
};

.CityObjects |= [
  to_entries | .[]
  | .value.parents |= if . then map("#:city-objects-\(.)") else empty end
  | { "@id": "#city-objects-\(.key | @uri)", "dct:identifier": .key } + .value
  | ."@id" as $OBJECT_ID
  | .geometry |= if . then ([ .[] |
    .type as $GEOM_TYPE | .boundaries as $BOUNDARIES | (try (.semantics.values | to_entries) catch []) as $INDEXES
    | {
      "surfaces": (if .semantics.surfaces
        then [.semantics.surfaces | to_entries | .[] | .key as $IDX
          | .value + {
            "@type": (if .type then [$GEOM_TYPE, .type] else $GEOM_TYPE end),
            "boundaries": ({"type": $GEOM_TYPE, "id": "\($OBJECT_ID)_geom_\($IDX)", "references": [$BOUNDARIES | .[$INDEXES | map(if .value == $IDX then .key else empty end) | .[]]]} | processBoundaries)
          }]
        else [{"@type": $GEOM_TYPE, "boundaries": ({"type": $GEOM_TYPE, "id": "\($OBJECT_ID)_geom_0", "references": $BOUNDARIES} | processBoundaries)}]
        end),
      "lod": "\(.lod)"
    }
  ]) else empty end
]
| . + {
  "@id": "#city"
}
|
def to_coords: if . then { "city:x": .[0], "city:y": .[1], "city:z": .[2] } else empty end ;
(.transform.scale |= to_coords) | (.transform.translate |= to_coords)
  | .metadata.geographicalExtent |= if . then {
    "city:min": .[0:3] | to_coords,
    "city:max": .[3:6] | to_coords
  } else empty end
  | .vertices |= [to_entries | .[] | {
    "@id": "#vertices-\(.key | @uri)",
    "type": "Feature",
    "geometry": {
      "@type": "Point",
      "geojson:coordinates": .value
    },
    "properties": (.value | to_coords),
  }]