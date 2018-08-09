from prometheus_client import start_http_server, Metric, REGISTRY
from re import split
import sys
import time
import subprocess

class CarbonCollector(object):
  def __init__(self):
      self._metric_group = "carbon/agent"

  def collect(self):
      output = subprocess.check_output('/prom_carbon_exporter/app/collector.py /prom_carbon_exporter/data', shell=True).split()

      intiate = Metric('', '', 'untyped')
      yield intiate

      for line in output:
          metric = line.decode("utf-8").split(",")
          if metric[2] == "None":
              value = float(metric[1])
          else:
              value = float(metric[2])
          metric_path = split('\/|\.wsp', metric[0])
          metric_name = 'carbon_agent_{}'.format(metric_path[4])
          labels = {}
          labels['host'] = metric_path[3]
          labels['metric'] = metric_path[5]
          if metric_name == "request_codes":
              labels['type'] = metric_path[6]
              labels['code'] = metric_path[7]
          metric = Metric(metric_name, '', 'untyped')
          metric.add_sample(metric_name, value=value, labels=labels)
          yield metric


if __name__ == '__main__':
  start_http_server(addr=sys.argv[1], port=int(sys.argv[2]))
  REGISTRY.unregister(REGISTRY._names_to_collectors['process_resident_memory_bytes'])
  REGISTRY.unregister(REGISTRY._names_to_collectors['python_info'])

  REGISTRY.register(CarbonCollector())

  while True: time.sleep(1)
