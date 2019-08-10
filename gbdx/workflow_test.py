import os
import gbdxtools
import boto3
gbdx = gbdxtools.Interface()


product_id = 'S2A_MSIL1C_20190321T171011_N0207_R112_T14TQL_20190322T001148'

sts = boto3.client('sts',
                   aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                   aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
temp_creds = sts.get_session_token(DurationSeconds=3600)['Credentials']


compile_archive_task = gbdx.Task('s2_compile_archive:0.0.2',
                                 image_id=product_id,
                                 aws_access_key_id=temp_creds['AccessKeyId'],
                                 aws_secret_access_key=temp_creds['SecretAccessKey'],
                                 aws_session_token=temp_creds['SessionToken'])

l2a_task = gbdx.Task('s2_L2A_process:0.0.2',
                     data=compile_archive_task.outputs.data.value,
                     resolution='20')

#band_stack
cmd = "mkdir $outdir/data1; "
cmd += "touch $outdir/data1/test.txt; "
cmd += "ls -al $indir/data1/; "
cmd += "gdal_merge.py -separate -of GTiff -o $outdir/data1/{product_id}.tif "
cmd += "$indir/data1/*.SAFE/GRANULE/*/IMG_DATA/R20m/*_B02_20m.jp2 "
cmd += "$indir/data1/*.SAFE/GRANULE/*/IMG_DATA/R20m/*_B03_20m.jp2 "
cmd += "$indir/data1/*.SAFE/GRANULE/*/IMG_DATA/R20m/*_B04_20m.jp2 "
cmd += "$indir/data1/*.SAFE/GRANULE/*/IMG_DATA/R20m/*_B05_20m.jp2 "
cmd += "$indir/data1/*.SAFE/GRANULE/*/IMG_DATA/R20m/*_B06_20m.jp2 "
cmd += "$indir/data1/*.SAFE/GRANULE/*/IMG_DATA/R20m/*_B07_20m.jp2 "
cmd += "$indir/data1/*.SAFE/GRANULE/*/IMG_DATA/R20m/*_B8A_20m.jp2 "
cmd += "$indir/data1/*.SAFE/GRANULE/*/IMG_DATA/R20m/*_B11_20m.jp2 "
cmd += "$indir/data1/*.SAFE/GRANULE/*/IMG_DATA/R20m/*_B12_20m.jp2; "
# set no data value
cmd += "gdal_edit.py -a_nodata 0 $outdir/data1/{product_id}.tif; "
cmd += "rm $outdir/data1/test.txt; "
cmd = cmd.format(product_id=product_id)
band_stack = gbdx.Task("gdal-cli-multiplex:0.0.1",
                       data1=l2a_task.outputs.data,
                       command=cmd)

tasks = [compile_archive_task,
         l2a_task,
         band_stack]

workflow = gbdx.Workflow(tasks)
# workflow.savedata(compile_archive_task.outputs.data, location='mgleason/s2_preprocessor_testing_20/compile_archive')
# workflow.savedata(l2a_task.outputs.data, location='mgleason/s2_preprocessor_testing_20/l2a')
workflow.savedata(band_stack.outputs.data1, location='mgleason/s2_preprocessor_testing_20/l2a_stacked/')
workflow.execute()

print(workflow.id)
print(os.path.join('s3://', 'gbd-customer-data',
                   gbdx.s3.info['prefix'], 'mgleason/s2_preprocessor_testing_20/l2a_stacked'))

