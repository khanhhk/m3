from math import ceil

from kubernetes import client
from prometheus_api_client import PrometheusConnect

# config.load_kube_config()
v1 = client.AppsV1Api()

import logging

import kopf

logging.basicConfig(level=logging.INFO)
import time

# Initialize connection to Prometheus
prom = PrometheusConnect(
    url="http://prometheus-operated.monitoring.svc.cluster.local:9090", disable_ssl=True
)


# Decide whether to scale up or down
def update_scale_status(resp, threshold, scale_up, scale_down):
    if resp > threshold:
        scale_up = True
    elif resp < threshold:
        scale_down = True

    return scale_up, scale_down


# Parse from YAML spec
def parse_spec(spec):
    interval = int(spec.get("interval", 1))
    query = spec.get("query", None)
    desiredMetricValue = spec.get("threshold", None)
    minReplicas = spec.get("minReplicas", 1)
    maxReplicas = spec.get("maxReplicas", 2)
    scaleTargetRef = spec.get("scaleTargetRef", None)

    return interval, query, desiredMetricValue, minReplicas, maxReplicas, scaleTargetRef


# Watch mmcontroller objects
@kopf.daemon("mmcontroller")
def monitor_resources(spec, stopped, **kwargs):
    # Parse configs from spec
    (
        interval,
        query,
        desiredMetricValue,
        minReplicas,
        maxReplicas,
        scaleTargetRef,
    ) = parse_spec(spec)

    # Raise error if any of necessary params are missing
    if not query:
        raise kopf.PermanentError(f"Query must be set. Got {query!r}.")

    if not desiredMetricValue:
        raise kopf.PermanentError(f"Threshold must be set. Got {desiredMetricValue!r}.")

    if not scaleTargetRef:
        raise kopf.PermanentError(
            f"scaleTargetRef must be set. Got {scaleTargetRef!r}."
        )

    # While the controller is still running
    while not stopped:
        # Query from Prometheus
        resp = prom.custom_query(query)

        # Sleep to retry if can not get metrics from Prometheus
        if len(resp) == 0:
            logging.info(
                f"Can not get response from from Prometheus. Trying again in {interval} seconds"
            )
        else:
            logging.info(f"Received response from from Prometheus!")
            currentMetricValue = float(resp[0]["value"][1])

            # Check whether it should scale down or scale up
            scale_up = False
            scale_down = False
            scale_up, scale_down = update_scale_status(
                currentMetricValue, desiredMetricValue, scale_up, scale_down
            )

            # Get the current number of replicas
            currentReplicas = client.CustomObjectsApi().get_namespaced_custom_object(
                group="serving.kserve.io",
                version="v1alpha1",
                namespace=scaleTargetRef["namespace"],
                plural="servingruntimes",
                name=scaleTargetRef["name"],
            )["spec"]["replicas"]

            # if scale up or scale down is needed
            if scale_up or scale_down:
                # Calculate desired replicas based on HPA metrics
                desiredReplicas = ceil(
                    currentReplicas * (currentMetricValue / desiredMetricValue)
                )

                # Reassign desired replicas based on min and max
                if desiredReplicas < minReplicas:
                    desiredReplicas = minReplicas
                elif desiredReplicas > maxReplicas:
                    desiredReplicas = maxReplicas

                # Only update if desiredRepicas is different from currentReplicas
                if desiredReplicas != currentReplicas:
                    if scale_up:
                        logging.info(
                            f"Scaling up replicas from {currentReplicas} to {desiredReplicas}"
                        )
                    elif scale_down:
                        logging.info(
                            f"Scaling down replicas from {currentReplicas} to {desiredReplicas}"
                        )

                    # Patch replicas of the ServingRuntimes
                    client.CustomObjectsApi().patch_namespaced_custom_object(
                        group="serving.kserve.io",
                        version="v1alpha1",
                        namespace=scaleTargetRef["namespace"],
                        plural="servingruntimes",
                        name=scaleTargetRef["name"],
                        body={"spec": {"replicas": desiredReplicas}},
                    )

        time.sleep(5)

    logging.info("We are done. Bye.")
