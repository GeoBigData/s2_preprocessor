from __future__ import absolute_import
import os
import json
import glob
from s2_preprocessor import L2A_process
from s2_preprocessor.utils import convert_type


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
    safes = glob.glob1(input_data, '*.SAFE')
    if len(safes) == 0:
        raise ValueError("No SAFE archive found in input data port")
    if len(safes) > 1:
        raise ValueError("Multiple SAFE archives found in input data port")
    in_safe = os.path.join(input_data, safes[0], '')

    # run the processing
    print("Starting L2A_Process...")
    L2A_process.main([in_safe,
                      out_path,
                      '--resolution', resolution])


if __name__ == '__main__':
    main()
