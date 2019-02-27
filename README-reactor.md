
# Build the reactor docker image

```
# The image tag must start with your Docker Hub organization
docker build --tag tcmitchell/sbh-metrics-reactor:0.1
```


# Test Locally

```
abaco deploy -R && scripts/run_container_message.sh message.sample.json
```


# Deploy reactor

You might have to refresh your tacc tokens...

```
# First, login to docker hub so the image can be pushed
docker login

# Next, deploy the actor
abaco deploy
```


# Invoke reactor

```
export MESSAGE=$(cat message.sample.json)
abaco submit -m "${MESSAGE}" z06e3lB5eGjbk
```
