import os
import gbdxtools
import boto3
gbdx = gbdxtools.Interface()


product_id = 'S2A_MSIL1C_20190321T171011_N0207_R112_T14TQL_20190322T001148'

sts = boto3.client('sts',
                   aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                   aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
temp_creds = sts.get_session_token(DurationSeconds=3600)['Credentials']


compile_archive_task = gbdx.Task('s2_compile_archive:0.0.1',
                                 image_id=product_id,
                                 aws_access_key_id=temp_creds['AccessKeyId'],
                                 aws_secret_access_key=temp_creds['SecretAccessKey'],
                                 aws_session_token=temp_creds['SessionToken'])

l2a_task = gbdx.Task('s2_L2A_process:0.0.1',
                     data=compile_archive_task.outputs.data.value,
                     resolution='60')

tasks = [compile_archive_task,
         l2a_task]

workflow = gbdx.Workflow(tasks)
workflow.savedata(compile_archive_task.outputs.data, location='mgleason/s2_preprocessor_testing/compile_archive')
workflow.savedata(l2a_task.outputs.data, location='mgleason/s2_preprocessor_testing/l2a')
workflow.execute()

print(workflow.id)
print(os.path.join('s3://', 'gbd-customer-data', gbdx.s3.info['prefix'], 'mgleason/s2_preprocessor_testing/compile_archive'))

