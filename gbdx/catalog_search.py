import gbdxtools
from sentinelhub import get_area_info, BBox, CRS, AwsTile, AwsTileRequest
gbdx = gbdxtools.Interface()


# Define search AOI and time period
search_bbox = BBox(bbox=[-95.9770, 40.9776, -95.7312, 41.0975], crs=CRS.WGS84)
search_time_interval = ('2019-03-17T00:00:00', '2019-03-21T23:59:59')

# Search for products
# Testing something different
print("Searching for Sentinel-2 scenes")
product_ids = []
for tile_info in get_area_info(search_bbox, search_time_interval, maxcc=0.5):
    tile_name, time, aws_index = AwsTile.tile_id_to_tile(tile_info['properties']['productIdentifier'])
    tile_request = AwsTileRequest(tile=tile_name, time=time, aws_index=aws_index,
                                  bands=None)
    safe_tile = tile_request.get_aws_service()
    product_id = safe_tile.get_product_id()
    product_ids.append(product_id)

print("{n} Sentinel-2 Scenes found..".format(n=len(product_ids)))
for product_id in product_ids:
    print("\tProduct ID: {}".format(product_id))


