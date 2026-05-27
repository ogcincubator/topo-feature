import json, geopandas as gpd
import sys
import glob as glob_module

from typing import Generator, List


def walk_features(data: list) -> Generator[dict, None, None]:
    """
    Walk features from a list of GeoJSON Features or FeatureCollections.

    Args:
        data: A list containing GeoJSON Feature or FeatureCollection objects

    Yields:
        Individual GeoJSON Feature dictionaries
    """
    for item in data:
        if isinstance(item, List):
            yield from  walk_features(item)
            continue
        elif isinstance(item, dict):
            match item.get("type"):
                case "Feature":
                    if "points" in item:
                        yield from walk_features(item.get("points", []))
                    else:
                        yield item
                case "FeatureCollection":
                    if "points" in item:
                        yield from walk_features(item.get("points", []))
                    else:
                        yield from walk_features(item.get("features", []))
                case _:
                    raise ValueError(f"Unexpected GeoJSON type: {item.get('type')!r}")
        else:
            yield item

def extract_feature_coordinates(data: list) -> dict[str, object]:
    """
    Extract a mapping of feature IDs to their coordinates as JSON strings.

    Args:
        data: A list containing GeoJSON Feature or FeatureCollection objects

    Returns:
        A dictionary mapping feature ID -> JSON-encoded coordinates
    """
    return {
        feature["id"]: feature["geometry"]["coordinates"]
        for feature in walk_features(data)
    }

def process(input_data,mode,number):
    if type(input_data) == str:
        data = json.loads(input_data)
    else:
        data = json.load(input_data)

    count = 0 # compare to number
    # Normalize: wrap a single Feature into a FeatureCollection
    is_feature = data.get("type") == "Feature"
    if is_feature:
        data = {"type": "FeatureCollection", "features": [data], "crs": data.get("crs")}

    # Extract CRS
    crs_name = ((data.get("crs") or {}).get("properties") or {}).get("name")
    epsg_code = crs_name.split(":")[-1] if crs_name else "4326"

    geomsmap = {}

    # transfer coordinates to features

    if "points" in data:
        # assume we nuke any features if points are explicit.
        data["features"] = []
        for pc in data["points"]:
            for feature in pc['features']:
                if 'id' in feature:
                    feature['properties']['feature_id'] = feature['id']
            if "points" in mode:
                data["features"].extend(pc["features"])
            geomsmap = extract_feature_coordinates(data["points"])
        # push ids to properties so geopandas doesnt nuke them
    elif "features" in data:
        # need to find points in features[] else cannot generate geometries
        pfeatures = []
        for feature in walk_features(data["features"]):
            if feature["type"] != "Point":
                pfeatures.append(feature)
        if len(pfeatures) > 0:
            if "points" in mode:
                data["features"] = list(pfeatures)
            else:
                data["features"] = []
            geomsmap = extract_feature_coordinates(pfeatures)

    if geomsmap == {}:
        raise ValueError("No point geometries found")

    geomtype = {"edges": "LineString", "solids": "Solid", "rings": "MultiLineString", "faces": "MultiPolygon" , "shells": "Solid"}
    for feat_type in [ "edges",  "rings" , "faces" ] :
        if not feat_type in data :
            continue
        for feat in walk_features ( data[feat_type] ):
            if "topology" in feat:
                # check type matches expected
                if feat["topology"]["type"].lower()+'s' != feat_type:
                    print("Warning expected type{} does not match {}".format(feat["topology"]["type"].lower(),feat_type))
                if "references" in feat["topology"] :
                    coords =  [ geomsmap[node] for node in feat["topology"]["references"] ]

                elif "directed_references" in feat["topology"] :
                    drs = feat["topology"]["directed_references"]
                    coords = [[]]
                    startindex = 0
                    for node in drs:
                        coordSet = geomsmap[node["ref"]][:]
                        if node["orientation"] == '-':
                            coords[0] += coordSet[::-1][startindex:]
                        else:
                            coords[0] += coordSet[startindex:]
                        if feat_type == 'edges':
                            # for lines skip starting point to join them up with duplicating end point
                            startindex = 1
                else:
                    print("No references found")
                    continue

                feat["geometry"] = {"type": geomtype[feat_type], "coordinates": coords, "properties": feat["properties"]}
                geomsmap[feat["id"]] = coords
                if feat_type in mode :
                    if number:
                        if count >= int(number):
                            continue
                    count +=1
                    data["features"].append(feat)



    # Create GeoDataFrame from GeoJSON-like dict
    if data["features"] == []:
        print("No feature geometries generated")
        return "{}"
    else:
        gdf = gpd.GeoDataFrame.from_features(data["features"])
    # Set CRS dynamically
    if epsg_code:
        gdf.set_crs(epsg=int(epsg_code), inplace=True)

    # Print current CRS
    print("Transform from CRS" + str(gdf.crs))

    # Transform to another CRS (example: ETRS89)
    if epsg_code != "4326":
        gdf = gdf.to_crs(epsg=4326)
        # Print current CRS
        print("            to CRS" + str(gdf.crs))

    # Convert back to GeoJSON — unwrap back to a single Feature if input was one
    result = json.loads(gdf.to_json())
    if is_feature == 1:
        outputstr = json.dumps(result["features"][0], indent=2)
    else:
        outputstr = gdf.to_json(indent=2)
    # JSON-LD enablement for viewer
    output_data = json.loads(outputstr)
    output_data["@context"] = [
        "https://opengeospatial.github.io/bblocks/annotated-schemas/geo/features/featureCollection/context.jsonld"
    ]
    if "@context" in data:
        context = data["@context"]
        if isinstance(context, List):
            iterable_data = context
        else:
            iterable_data = [context]
        for c in iterable_data:
            output_data["@context"].append(c)
    return json.dumps(output_data, indent=2)

testmode = True
try:
    if 'mode' in transform_metadata.metadata:
        mode = transform_metadata.metadata["mode"]
except:
    mode = "points,edges,faces"


try:
    if input_data:
        print("running in transformer mode")
    output_data = process(input_data,mode,None)
    testmode = False
except:
    mode = "points,edges,faces"
    testmode = True

if __name__ == "__main__" and testmode:
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--input_data', help="input file")
    argparser.add_argument('-o', '--output_file', help="output file")
    argparser.add_argument('-p', '--print', action='store_true', help="Print output of each file")
    argparser.add_argument('-n', '--number', default=None, help="Count of features to process")
    argparser.add_argument('-m', '--mode', default="points,edges,faces", help="points,edges,faces (comma separated list)")
    args = argparser.parse_args()
    if args.input_data:
        for f in sorted(glob_module.glob(args.input_data)):
            print("Processing {}".format(f))
            input_data = open(f, "r").read()
            output_data = process(input_data, args.mode, args.number)
            if args.print:
                print(output_data)
    else:
        print("No input file")



