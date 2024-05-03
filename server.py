from kubernetes import client, config
from flask import Flask,request, jsonify
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
app = Flask(__name__)
batch_v1 = client.BatchV1Api()
# app.run(debug = True)

def create_job_from_yaml(yaml_file, namespace):
    with open(yaml_file) as f:
        job = yaml.safe_load(f)
        # Adjust namespace if necessary
        job['metadata']['namespace'] = namespace
        # Create the job in Kubernetes
        response = batch_v1.create_namespaced_job(body=job, namespace=namespace)
        return response

@app.route('/config', methods=['GET'])
def get_config():
    pods = []

    # your code here
    
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for pod in ret.items:
        pod_info = {
            "node": pod.spec.node_name,
            "ip": pod.status.pod_ip,
            "namespace": pod.metadata.namespace,
            "name": pod.metadata.name,
            "status": pod.status.phase
        }
        pods.append(pod_info)
    output = {"pods": pods}
    output = json.dumps(output)

    return output

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    create_job_from_yaml('free-service-job.yaml', 'free-service')

    return jsonify({"message": "Free service job submitted successfully"}), 200


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here
    create_job_from_yaml('premium-service-job.yaml', 'default')
    return jsonify({"message": "Premium service job submitted successfully"}), 200

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
