import kubernetes
import sys

def check_deployment_replication_status(config_file, namespace, deployment_name):
    conf = kubernetes.config.load_kube_config(config_file=config_file)

    with kubernetes.client.ApiClient(conf) as api_client:
        api_instance = kubernetes.client.AppsV1Api(api_client)

        try:
            api_response = api_instance.read_namespaced_deployment_status(deployment_name, namespace, pretty="true")

            if api_response.status.replicas != api_response.status.ready_replicas \
                or api_response.status.unavailable_replicas:
                print("Planned replicas: {}\nReady replicas: {}\nUnavailable replicas: {} \
                ".format(api_response.status.replicas,api_response.status.ready_replicas, \
                api_response.status.unavailable_replicas))
                raise Exception("Deployment {} has incorrect number of replicas.".format(deployment_name))

        except kubernetes.client.rest.ApiException as e:
            raise Exception ("Exception when calling AppsV1Api->read_namespaced_deployment_status: %s\n" % e)
        
        print("Deployment {} has passed liveliness check.".format(deployment_name))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Incorrect arguments. Usage: python check_deployment_status.py [namespace] [kube-config-file]")
    
    check_deployment_replication_status(sys.argv[2], sys.argv[1], "kibana")
    check_deployment_replication_status(sys.argv[2], sys.argv[1], "elasticsearch")
    check_deployment_replication_status(sys.argv[2], sys.argv[1], "logstash")
    check_deployment_replication_status(sys.argv[2], sys.argv[1], "filebeat")
