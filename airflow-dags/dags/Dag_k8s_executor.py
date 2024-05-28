from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from kubernetes.client import models as k8s

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'example_kubernetes_executor_dag',
    default_args=default_args,
    description='A simple DAG with Kubernetes Executor and multiple volume mounts',
    schedule_interval=None,
    tags=['example'],
)

# Define a simple Python function to run as a task
def print_hello():
    print("Hello from Kubernetes Executor with multiple volume mounts!")

# Create a PythonOperator task with custom executor config
hello_task = PythonOperator(
    task_id='hello_task',
    python_callable=print_hello,
    dag=dag,
    executor_config={
        "KubernetesExecutor": {
            "image": "your-docker-repo/airflow-worker:latest",
            "namespace": "airflow",
            "env_vars": {
                "EXAMPLE_ENV_VAR": "example_value"
            },
            "volume_mounts": [
                k8s.V1VolumeMount(
                    name="example-volume-1",
                    mount_path="/path/inside/container1"
                ),
                k8s.V1VolumeMount(
                    name="example-volume-2",
                    mount_path="/path/inside/container2"
                )
            ],
            "volumes": [
                k8s.V1Volume(
                    name="example-volume-1",
                    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
                        claim_name="example-claim-1"
                    )
                ),
                k8s.V1Volume(
                    name="example-volume-2",
                    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(
                        claim_name="example-claim-2"
                    )
                )
            ],
        }
    },
)

# Set the task
hello_task
