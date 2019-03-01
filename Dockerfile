FROM sd2e/reactors:python3
# FROM sd2e/reactors:python3-edge

# reactor.py, config.yml, and message.jsonschema will be automatically
# added to the container when you run docker build or abaco deploy

# Uninstall synbiohub_adapter and friends
#   I'm erring on the side of caution, I'm not sure all three have to be uninstalled
RUN pip3 uninstall -y synbiohub_adapter pySBOLx pysbol

# Now install the latest synbiohub_adapter
RUN pip3 install \
      --process-dependency-link \
      git+https://github.com/SD2E/synbiohub_adapter.git

ADD sbh-metrics.py /sbh-metrics.py
ADD sd2 /sd2
ADD reactor.ini /reactor.ini
