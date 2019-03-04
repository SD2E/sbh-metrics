
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

At the end of the deploy, the actor id is displayed.


# Invoke reactor

```
export MESSAGE=$(cat message.sample.json)
abaco submit -m "${MESSAGE}" ACTOR_ID
```

After the submit an execution id is displayed.


# View logs after run

```
abaco logs ACTOR_ID EXECUTION_ID
```


# Agave Basics

```
# List the user area (substitute your name for "user")
files-list -S data-tacc-work-user

# Make a directory
files-mkdir -S data-tacc-work-tmitchel -N sd2metrics

# List the new directory
files-list -S data-tacc-work-tmitchel sd2metrics

# Upload a file to the new directory
files-upload -S data-tacc-work-tmitchel -F ../data/TriplesMetric.csv sd2metrics
```
