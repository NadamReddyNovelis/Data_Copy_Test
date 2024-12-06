import os
from datetime import datetime
import pytz

from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs

workspace_id = os.getenv("WORKSPACE_INSTANCE")
api_token = os.getenv("WORKSPACE_TOKEN")
job_id = os.getenv("JOB_ID")

def trigger_job_run_sdk(job_id, params):
    try:
        run = workspace_client.jobs.run_now(
            job_id=job_id,
            notebook_params=params
        )
        print(f'Triggered a job run with run_id: {run.response.run_id}')
        
        run_res = run.result().as_dict()
        return {key: run_result.get(key) for key in ['run_id', 'run_page_url', 'state']}
    except Exception as e:
        raise Exception(f'Failed to trigger workflow run: {e}')

if __name__ == '__main__':
    base_uri = f'https://adb-{workspace_id}.azuredatabricks.net/'
    workspace_client = WorkspaceClient(
        host=base_uri,
        token=api_token,
    )

    run_result = trigger_job_run_sdk(job_id=job_id, params=params)
    
    print(f'Job at: {run_result["run_page_url"]} completed with result state: {run_result["state"]}')
    if run_result['state'] in ('SUCCESSFUL'):
        pass
    else:
        raise Exception('Job run failed.')
        
