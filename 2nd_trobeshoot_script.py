# pip install cryptography==3.3.2
# pip install kubernetes==26.1.0
import kubernetes
from kubernetes import client, config

# Load the Kubernetes configuration from the default location
config.load_kube_config()

# Create the Kubernetes API client
api_client = client.ApiClient()

# Check for pod errors
v1 = client.CoreV1Api(api_client)
pod_list = v1.list_pod_for_all_namespaces(watch=False)
for pod in pod_list.items:
    if pod.status.phase != 'Running':
        print(f"Error in Pod {pod.metadata.name}: {pod.status.phase}")
    for container_status in pod.status.container_statuses:
        if container_status.state.waiting:
            print(f"Error in Pod {pod.metadata.name}, container {container_status.name}: {container_status.state.waiting.reason}")
        elif container_status.state.terminated:
            print(f"Error in Pod {pod.metadata.name}, container {container_status.name}: {container_status.state.terminated.reason}")

# Check for deployment errors
v1_beta = client.AppsV1Api(api_client)
deployment_list = v1_beta.list_deployment_for_all_namespaces(watch=False)
for deployment in deployment_list.items:
    if deployment.status.unavailable_replicas:
        print(f"Error in Deployment {deployment.metadata.name}: {deployment.status.unavailable_replicas} unavailable replicas")

# Check for statefulset errors
v1_apps = client.AppsV1Api(api_client)
statefulset_list = v1_apps.list_stateful_set_for_all_namespaces(watch=False)
for statefulset in statefulset_list.items:
    if statefulset.status.current_replicas != statefulset.status.ready_replicas:
        print(f"Error in StatefulSet {statefulset.metadata.name}: {statefulset.status.current_replicas} current replicas, {statefulset.status.ready_replicas} ready replicas")

# Check for volume errors
v1 = client.CoreV1Api(api_client)
pvc_list = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)
for pvc in pvc_list.items:
    if pvc.status.phase != 'Bound':
        print(f"Error in Persistent Volume Claim {pvc.metadata.name}: {pvc.status.phase}")

pv_list = v1.list_persistent_volume(watch=False)
for pv in pv_list.items:
    if pv.status.phase != 'Bound':
        print(f"Error in Persistent Volume {pv.metadata.name}: {pv.status.phase}")
