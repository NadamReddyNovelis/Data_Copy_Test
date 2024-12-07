import os
import json
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs


def trigger_job_run_sdk(job_id, params):
    try:
        run = workspace_client.jobs.run_now(
            job_id=job_id,
            notebook_params=params
        )
        print(f'Triggered a job run with run_id: {run.response.run_id}')
        
        run_res = run.result().as_dict()
        return {key: run_res.get(key) for key in ['run_id', 'run_page_url', 'state']}
    except Exception as e:
        raise Exception(f'Failed to trigger workflow run: {e}')


if __name__ == '__main__':
    workspace_id = os.getenv("WORKSPACE_INSTANCE")
    api_token = os.getenv("WORKSPACE_TOKEN")
    job_id = os.getenv("JOB_ID")
    params = os.getenv("NOTEBOOK_PARAMS")
    try:
        if type(params) == str:
            params = json.loads(params)
        elif type(params) == dict:
            pass
        else:
            raise Exception(f'{type(params)} - is not valid for notebook params')
    except json.JSONDecodeError as e:
        print(f"Invalid format for a JSON Object: {e}")
        raise
    except Exception as e:
        print(f"Invalid format for notebook params: {e}")
        raise
        
    base_uri = f'https://adb-{workspace_id}.azuredatabricks.net/'
    workspace_client = WorkspaceClient(
        host=base_uri,
        token=api_token,
    )
    try:
        run_result = trigger_job_run_sdk(job_id=job_id, params=params)
    
        print(f'Job at: {run_result["run_page_url"]} completed with result state: {run_result["state"]}')
        if run_result["state"].get("result_state",run_result["state"].get("life_cycle_state")) not in ('SUCCESS'):
            raise Exception('Job Status - FAILED')
    except Exception as e:
        raise Exception(f'Error: {e}')
