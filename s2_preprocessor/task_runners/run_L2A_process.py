from __future__ import absolute_import
import os
import json
import glob
from s2_preprocessor import L2A_process
from s2_preprocessor.utils import convert_type
import sh

def main():

    # get the inputs
    string_ports = '/mnt/work/input/ports.json'
    input_data = '/mnt/work/input/data'

    # create output directory
    out_path = '/mnt/work/output/data'
    if os.path.exists(out_path) is False:
        os.makedirs(out_path)

    # read the inputs
    with open(string_ports) as ports:
        inputs = json.load(ports)
    resolution = inputs.get('resolution', 20)

    # convert the inputs to the correct dtypes
    resolution = convert_type(resolution, int, 'Int')

    # get the SAFE file in the input folder
    zips = glob.glob1(input_data, '*.zip')
    if len(zips) == 0:
        raise ValueError("No zips found in input data port")
    if len(zips) > 1:
        raise ValueError("Multiple zips found in input data port")
    in_zip = os.path.join(input_data, zips[0])

    # unzip it
    sh.unzip(in_zip, _cwd=os.path.dirname(in_zip))

    # rename to safe
    in_safe = in_zip.replace('.zip', '.SAFE')

    # run the processing
    print("Starting L2A_Process...")
    L2A_process.main([in_safe,
                      out_path,
                      '--resolution', resolution])


if __name__ == '__main__':
    main()
