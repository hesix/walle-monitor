# VERSION:	0.1
# AUTHOR:	Xiaotian Wu
# DESCRIPTION:	Image of walle-monitor, walle is the
#               log-collector service of ChinaCache

# all service running on mesos should be inherited from mesos-executor
FROM cpdc/matrix-executor
MAINTAINER Xiaotian Wu <xiaotian.wu@chinacache.com>

# install modified kafka-python for special usage
RUN git clone https://github.com/cpdc/kafka-python
RUN cd kafka-python&&python setup.py install

# for influxdb-python
RUN easy_install pip
RUN pip install influxdb

# walle-monitor
ADD . /walle-monitor
ENV WALLE_MONITOR_PATH /walle-monitor
ENV PYTHONPATH /walle-monitor
