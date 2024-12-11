import os, sys
import json
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs


def trigger_job_run_sdk(job_id, params):
    try:
        run = workspace_client.jobs.run_now(
            job_id=job_id,
            notebook_params=params
        )
    except Exception as e:
        raise Exception(f'Failed to trigger workflow run: {e}')
    
    print(f'Triggered a job run with run_id: {run.response.run_id}')
    
    run_res = run.result().as_dict()
    return {key: run_res.get(key, 'Key-Unavailable') for key in ['run_id', 'run_page_url', 'state']}


if __name__ == '__main__':
    job_id = os.getenv("JOB_ID")
    params = sys.argv[1]
    try:
        if type(params) == str:
            params = json.loads(params)
        elif type(params) == dict:
            pass
        else:
            raise Exception(f'{params} of type: {type(params)} - is not valid for notebook params')
    except json.JSONDecodeError as e:
        print(f"Invalid format for a JSON Object: {e}")
        raise
    except Exception as e:
        print(f"Invalid format for notebook params: {e}")
        sys.exit(1)
        
    workspace_client = WorkspaceClient()
    try:
        run_result = trigger_job_run_sdk(job_id=job_id, params=params)
    
        print(f'Job at: {run_result["run_page_url"]} completed with state: {run_result["state"]}')
        msg = lambda status: f'Job exited with result state - {run_result["state"].get("result_state")} | Status - {status}'
        if run_result["state"].get("result_state") not in ('SUCCESS'):
            raise Exception(msg('FAILED'))
        else: print(msg('SUCCESS'))
    except Exception as e:
        raise Exception(f'Error: {e}')
