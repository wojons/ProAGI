from typing import Optional, Dict, Any, List
import prometheus_client
import threading # Potentially needed for running the metrics server in a separate thread
import time # Potentially needed for timing metrics

# Import necessary data models from core.shared.data_models
from core.shared.data_models.data_models import Metric # Assuming Metric data model exists (Issue #XX)

from core.interfaces.metric_collector_interface import MetricCollectorInterface

class MetricCollector(MetricCollectorInterface):
    """
    Collects and exposes operational metrics for the Nexus CoCreate AI framework and applications.
    It uses the `prometheus_client` library to manage metrics and provides methods
    to update counters, gauges, and histograms. Metrics can be exposed in Prometheus
    exposition format.
    """
    def __init__(self):
        """
        Initializes the MetricCollector with a Prometheus CollectorRegistry and internal dictionaries
        to keep track of registered metrics.
        """
        self._registry = prometheus_client.CollectorRegistry()
        self._counters: Dict[str, prometheus_client.Counter] = {}
        self._gauges: Dict[str, prometheus_client.Gauge] = {}
        self._histograms: Dict[str, prometheus_client.Histogram] = {}
        print("MetricCollector initialized.") # Basic logging
        # TODO: Consider starting a separate thread/process for an HTTP server to expose metrics (Issue #XX)
        # if needed for direct scraping by Prometheus. For now, metrics can be generated
        # on demand via the generate_latest_metrics method.

    def _get_or_create_counter(self, name: str, labelnames: list[str]) -> prometheus_client.Counter:
        """
        Retrieves an existing Counter metric or creates a new one if it doesn't exist.

        Args:
            name: The name of the counter metric.
            labelnames: A list of label names for the metric.

        Returns:
            A Prometheus Counter object.
        """
        if name not in self._counters:
            print(f"Creating new counter metric: {name} with labels {labelnames}") # Basic logging
            self._counters[name] = prometheus_client.Counter(
                name,
                f'Counter metric for {name}', # TODO: Add more descriptive help text (Issue #XX)
                labelnames=labelnames,
                registry=self._registry
            )
        return self._counters[name]

    def _get_or_create_gauge(self, name: str, labelnames: list[str]) -> prometheus_client.Gauge:
        """
        Retrieves an existing Gauge metric or creates a new one if it doesn't exist.

        Args:
            name: The name of the gauge metric.
            labelnames: A list of label names for the metric.

        Returns:
            A Prometheus Gauge object.
        """
        if name not in self._gauges:
            print(f"Creating new gauge metric: {name} with labels {labelnames}") # Basic logging
            self._gauges[name] = prometheus_client.Gauge(
                name,
                f'Gauge metric for {name}', # TODO: Add more descriptive help text (Issue #XX)
                labelnames=labelnames,
                registry=self._registry
            )
        return self._gauges[name]

    def _get_or_create_histogram(self, name: str, labelnames: list[str]) -> prometheus_client.Histogram:
        """
        Retrieves an existing Histogram metric or creates a new one if it doesn't exist.

        Args:
            name: The name of the histogram metric.
            labelnames: A list of label names for the metric.

        Returns:
            A Prometheus Histogram object.
        """
        if name not in self._histograms:
            print(f"Creating new histogram metric: {name} with labels {labelnames}") # Basic logging
            # TODO: Define appropriate buckets based on expected values for different metrics (Issue #XX)
            self._histograms[name] = prometheus_client.Histogram(
                name,
                f'Histogram metric for {name}', # TODO: Add more descriptive help text (Issue #XX)
                labelnames=labelnames,
                registry=self._registry
            )
        return self._histograms[name]

    async def increment_counter(self, name: str, labels: Optional[Dict[str, str]] = None):
        """
        Increments a counter metric by 1.

        Args:
            name: The name of the counter metric.
            labels: Optional dictionary of label key-value pairs.
        """
        labelnames = list(labels.keys()) if labels else []
        try:
            counter = self._get_or_create_counter(name, labelnames)
            if labels:
                counter.labels(**labels).inc()
            else:
                counter.inc()
            # print(f"Incremented counter: {name} with labels {labels}") # Optional: Log every increment
        except Exception as e:
            print(f"Error incrementing counter {name} with labels {labels}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)


    async def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """
        Sets the value of a gauge metric.

        Args:
            name: The name of the gauge metric.
            value: The value to set.
            labels: Optional dictionary of label key-value pairs.
        """
        labelnames = list(labels.keys()) if labels else []
        try:
            gauge = self._get_or_create_gauge(name, labelnames)
            if labels:
                gauge.labels(**labels).set(value)
            else:
                gauge.set(value)
            # print(f"Set gauge: {name} to {value} with labels {labels}") # Optional: Log every set
        except Exception as e:
            print(f"Error setting gauge {name} to {value} with labels {labels}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)


    async def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """
        Observes a value for a histogram metric.

        Args:
            name: The name of the histogram metric.
            value: The value to observe.
            labels: Optional dictionary of label key-value pairs.
        """
        labelnames = list(labels.keys()) if labels else []
        try:
            histogram = self._get_or_create_histogram(name, labelnames)
            if labels:
                histogram.labels(**labels).observe(value)
            else:
                histogram.observe(value)
            # print(f"Observed histogram: {name} with value {value} and labels {labels}") # Optional: Log every observe
        except Exception as e:
            print(f"Error observing histogram {name} with value {value} and labels {labels}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)


    def generate_latest_metrics(self) -> bytes:
        """
        Generates the latest collected metrics in Prometheus exposition format.
        This method is synchronous as per prometheus_client's design.

        Returns:
            Bytes containing the metrics in Prometheus text format.
        """
        print("Generating latest metrics.") # Basic logging
        try:
            return prometheus_client.generate_latest(self._registry)
        except Exception as e:
            print(f"Error generating latest metrics: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            return b"" # Return empty bytes on error

    # TODO: Add methods for collecting system-level metrics if needed (CPU, memory, network) (Issue #XX)
    # This might involve using libraries like psutil.
    # TODO: Implement a push gateway integration or an internal HTTP server for scraping (Issue #XX)
