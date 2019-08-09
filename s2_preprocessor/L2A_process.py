import click
import sh
import sys

@click.command()
@click.argument('input_dir')
@click.argument('output_dir')
@click.option('--resolution', '-r', required=False, type=int, default=20,
              help="Resolution in meters for output rasters. Options are 10, 20, and 60. Default: 20.")
def main(input_dir, output_dir, resolution=20):

    valid_resolutions = (10, 20, 60)
    if resolution not in valid_resolutions:
        err = "Specified resolution {resolution} is not valid. Must be one of {valid_resolutions}".format(
                resolution=resolution,
                valid_resolutions=valid_resolutions)
        raise ValueError(err)

    process_args = [input_dir,
                    '--output_dir', output_dir,
                    '--resolution', resolution]
    sh.L2A_Process(process_args,
                   _out=sys.stdout)

if __name__ == '__main__':
    main()