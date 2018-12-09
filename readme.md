# gbdx catalog search service #
This is a service written in python3 that accesses the gbdx API to retrieve catalogs that match an area given by a geojson.
## docker-compose deployment ##
__Requirements:__ docker, docker-compose

__Steps__:
1. Set gbdx credentials in _.env_ file
2. Deploy container locally: `docker-compose up`
3. Test the api using curl: `curl -X POST --data "@./aoi.geojson" localhost:5000/search`

## K8 deployment ##
This guide is based on minikube, but is easily adaptable to other K8 installations.

__Requirements:__ docker, k8, minikube

__Steps:__
1. Activate ingress controller: `minikube addons enable ingress`(if you do not use minikube, any cluster with an ingress controller will suffice)
2. Build the docker image and make it available inside the cluster (steps take from: https://stackoverflow.com/questions/42564058/how-to-use-local-docker-images-with-minikube):
   1. Connect with docker inside K8: `eval $(minikube docker-env)`
   2. Build image: `docker build -t gbdx_catalog_search .`
3. Create secret for gbdx credentials: `kubectl create secret generic gbdx-secret --from-literal=GBDX_USER='<username>' --from-literal=GBDX_PASSWORD='<password>'`
4. Apply K8 artefacts: `kubectl apply -f ./kubernetes`
5. Determine cluster ip: `minikube ip`
6. Test the api using curl: `curl -L -k -X POST --data "@./aoi.geojson" <cluster ip>/gbdx-catalog/search`. _-L_ enables following redirects which is necessary because the ingress controller may redirect http to https automatically. _-k_ turns off the ssl certifacte check, the check would fail because the ingress controller may use a self signed certificate.
7. An autoscaler is defined in _./kubernetes/autoscaler.yml_. Alternatively you can simply use kubectl: `kubectl scale deployment gbdx-deployment --replicas 3`
