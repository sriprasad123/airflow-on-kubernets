from kubernetes.client import models as k8s

# Define a simple Python function to run as a task
def print_hello():
    print("Hello from Kubernetes Executor!")

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
            "volume_mounts": [k8s.V1VolumeMount(name="example-volume", mount_path="/example_path")],
            "volumes": [k8s.V1Volume(name="example-volume", persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name="example-claim"))],
        }
    },
)
