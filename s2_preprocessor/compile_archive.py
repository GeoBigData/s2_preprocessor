import click
from sentinelhub import AwsProductRequest
import os
import sh

@click.command()
@click.argument('image_id')
@click.argument('out_path')
@click.option('--aws_access_key_id', '-K', required=False, type=str, default=None,
              help="If provided, AWS_ACCESS_KEY_ID configuration variable will be set at runtime."
                   "If not provided, sentinelhub will try to use pre-existing information in config file.")
@click.option('--aws_secret_access_key', '-S', required=False, type=str, default=None,
              help="If provided, AWS_SECRET_ACCESS_KEY environment variable will be set at runtime."
                   "If not provided, sentinelhub will try to use pre-existing information in config file.")
@click.option('--aws_session_token', '-T', required=False, type=str, default=None,
              help="If provided, AWS_SESSION_TOKEN environment variable will be set at runtime."
                   "If not provided, sentinelhub will try to use pre-existing information in config file.")
@click.option('--tiles', '-t', required=False, type=str, default=None,
              help="Tiles to download, provided as a comma-delimited string."
                   "If not specified, all tiles will be downloaded. ")
@click.option('--bands', '-b', required=False, type=str, default=None,
              help="Bands to download, provided as a comma-delimited string."
                   "If not specified, all bands will be downloaded. ")
def main(image_id, out_path, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None,
         tiles=None, bands=None):
    """Download data from AWS open data and convert into SAFE format compatible with ESA tools"""

    # set environment variables to enable AWS access
    os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
    os.environ['AWS_SESSION_TOKEN'] = aws_session_token

    # parse input args
    if tiles is not None:
        tile_list = map(str, tiles.split(','))
    else:
        tile_list = None

    if bands is not None:
        band_list = map(str, bands.split(','))
    else:
        band_list = None

    print("Compiling SAFE archive for {}...".format(image_id))
    product_request = AwsProductRequest(product_id=image_id, data_folder=out_path, safe_format=True,
                                        tile_list=tile_list, bands=band_list)
    product_request.save_data()

    # zip it all up
    # necessary because otherwise gbdx will drop empty folders and sen2cor will fail
    print("Zipping up SAFE archive")
    archive = os.path.join(out_path, '{}.SAFE'.format(image_id))
    # use sh to do this because the shutil.make_archive() function doesn't seem to work with SNAP
    sh.zip('-rm', archive.replace('.SAFE', '.zip'), os.path.basename(archive), '-4', _cwd=os.path.dirname(archive))

    print("Process completed successfully.")


if __name__ == '__main__':
    main()

