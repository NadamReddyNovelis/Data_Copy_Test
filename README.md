# **DAP_DATA_COPY**

*_Data-Copy Activity - CLONE | CREATE_ : From one Databricks workspace to another (Higher ENV to Lower ENV)*

---

## Repository Structure

```
|-- root-directory/
    |-- .github/
        |-- workflows/                                # Workflow configuration files for GitHub Actions
            |-- trigger_dbr_workflow-Data_Copy.yml    # GitHub Actions Workflow file for - Data_Copy Activity
    |-- src/
        |-- databricks_workflow_trigger.py            # Python script to trigger Databricks workflows
    |-- requirements.txt                              # List of Python dependencies to be installed on the workflow runner
```

## Steps to Run the Workflows

### Triggering the Workflow

The GitHub Actions workflow leverages the `workflow_dispatch` feature to allow manual triggering with user inputs. Follow the steps below:

1. Navigate to the **GitHub Actions** tab in your repository.
2. Select the workflow titled - **_Data-Copy - Trigger Job-run_**.
3. Choose the appropriate branch from the dropdown (**DEV**, **QA**, or **PROD**). The workflow must be triggered only from one of these branches as the **main** branch is for source code only and cannot be used to trigger workflows.
4. Click **Run Workflow** and provide the following inputs:

#### Workflow Inputs

| Input Name                     | Description                                            | Required | Notes                                                                                      |
| ------------------------------ | ------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------ |
| **OPERATION_TYPE**             | Type of operation to perform: **CLONE** or **CREATE**. | Yes      | Specifies which activity to be performed - `CLONE` / `CREATE`.                             |
| **FROM_ENV**                   | Source environment to copy data from.                  | Yes      | Must be a higher environment than `TO_ENV`. Options: (dependent on branch).                |
| **TO_ENV**                     | Target environment to copy data to.                    | Yes      | Must be a lower environment than `FROM_ENV`. Options:  (dependent on branch).              |
| **INGESTION_LAYER**            | The ingestion layer being processed                    | Yes      | `S` - STAGING / `SS` - SOURCE STAGING / `ENT` - `ENTERPRISE` / `SCHEMA-NAME`               |
| **COMMA SEPARATED TABLE LIST** | List of tables (comma-separated) to copy.              | Yes      | Must be provided regardless of the ingestion layer.                                        |
| **REGION**                     | Region to process data for.                            | No       | Only applicable if the `INGESTION_LAYER` is **SS**.                                        |
| **SYSTEM**                     | System identifier to process data for.                 | No       | Only applicable if the `INGESTION_LAYER` is **SS**.                                        |
| **PLANT**                      | Plant identifier to process data for.                  | No       | Only applicable if the `INGESTION_LAYER` is **SS**.                                        |

#### Input Dependencies

- **FROM\_ENV** and **TO\_ENV** dropdown values depend on the branch:
  - For **PROD** branch: `FROM_ENV` is **PROD**, `TO_ENV` can be [**QA**, **PREPROD**, **SIT**, **DEV**]
  - For **QA** branch: `FROM_ENV` can be [**QA**, **PREPROD**] `TO_ENV` can be [**QA**, **PREPROD**, **SIT**, **DEV**]
  - For **DEV** branch: `FROM_ENV` can be [**SIT**, **DEV**] and `TO_ENV` can be [**SIT**, **DEV**]
    
- **REGION**, **SYSTEM**, and **PLANT** inputs are only applicable if `INGESTION_LAYER` is **SS** (Source Staging).

5. Click **Run Workflow** after providing the required inputs. The workflow will execute and trigger a job run in Databricks.

### Monitoring the Workflow

- Check the GitHub Actions page and select the triggered run for live logs and the status of the workflow execution.
- The workflow run contains the following tasks:
  - **`Debug-Input-Params`** - Verify the input params passed to the workflow.
  - **`Validate-Params`** - Performs some basic validations on the input params before actually proceeding with the workflow.
  - **`Trigger-Workflow`** - Executes the _databricks_workflow_trigger.py_ with provided inputs and databricks variables configured in the environment associated with the branch.
    - If a databricks job was triggered successfully - Job failure causes the task to fail. Check the Databricks Job-run created for this for further analysis.
    - Upon successful initiation of the workflow a Databricks job run is triggered in the intended workflow.
- For the **run_id** / **run_url** / **Job-Status** - Check the logs under **`Trigger-Workflow`**

---

## Branches Description

| Branch Name | Purpose                                                           |
| ----------- | ----------------------------------------------------------------- |
| **main**    | Master branch. Not meant to be used to trigger the workflow       |
| **PROD**    | Branch to trigger runs in `PROD` workspace                        |
| **QA**      | Branch to trigger runs in `QA` workspace                          |
| **DEV**     | Branch to trigger runs in `DEV` workspace                         |

---
