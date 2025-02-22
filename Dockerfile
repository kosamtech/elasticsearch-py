FROM docker.elastic.co/elasticsearch/elasticsearch:8.17.2

# Override the default memory of 50% of system memory -> 3Gi
RUN echo "-Xms3g" > /usr/share/elasticsearch/config/jvm.options.d/heap.options && \
    echo "-Xmx3g" > /usr/share/elasticsearch/config/jvm.options.d/heap.options

