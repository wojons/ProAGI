from typing import Optional, Dict, Any
import json
import logging
from datetime import datetime # Needed for timestamp if not provided in LogMessage

# Import necessary data models from core.shared.data_models
from core.shared.data_models.data_models import LogMessage # Assuming LogMessage data model exists (Issue #XX)

from core.interfaces.logging_service_interface import LoggingServiceInterface

# Custom JSON formatter for Python logging
class JsonFormatter(logging.Formatter):
    """
    A custom logging formatter that formats log records as JSON strings.
    Includes mandatory context fields and allows for additional metadata.
    """
    def format(self, record):
        """
        Formats a log record into a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON string representing the log record.
        """
        # Use record creation time as the primary timestamp
        timestamp = datetime.fromtimestamp(record.created).isoformat()

        log_record = {
            "timestamp": timestamp,
            "level": record.levelname.lower(),
            "message": record.getMessage(),
            "component_name": record.name, # Use logger name as component_name by default
            # Mandatory context fields (will be populated from LogMessage metadata if available)
            "traceId": getattr(record, 'traceId', None),
            "appId": getattr(record, 'appId', None),
            "requestId": getattr(record, 'requestId', None),
            # Include other LogMessage fields if they are passed as extra/metadata
            "taskId": getattr(record, 'taskId', None),
            "context": getattr(record, 'context', None),
            # Include any other extra attributes passed in 'extra' dictionary
            **getattr(record, 'metadata', {}) # Include metadata from LogMessage or other extra
        }
        # Filter out None values for cleaner output
        log_record = {k: v for k, v in log_record.items() if v is not None}
        return json.dumps(log_record)


class LoggingService(LoggingServiceInterface):
    """
    Provides structured logging capabilities for the Core Framework and application sandboxes.
    It collects, processes, and outputs log messages in a standardized JSON format.
    Uses Python's built-in logging module with a custom formatter.
    """
    def __init__(self):
        """
        Configures the Python logger for structured JSON output to the console.
        Initializes the root logger for the framework.
        """
        self._logger = logging.getLogger("nexus_cocreate_ai") # Get a root logger for the framework
        self._logger.setLevel(logging.INFO) # Set default logging level (TODO: Make configurable - Issue #XX)

        # Prevent adding multiple handlers if already configured (important for re-initialization)
        if not self._logger.handlers:
            console_handler = logging.StreamHandler()
            formatter = JsonFormatter()
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

        print("LoggingService initialized with JSON console output.") # Basic logging

    async def log_framework_message(
        self,
        level: str,
        message: str,
        component_name: str,
        traceId: Optional[str] = None,
        appId: Optional[str] = None,
        requestId: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Logs a structured message originating from the Core Framework components.
        This method is used by framework components to report their own status and errors.

        Args:
            level: The logging level (e.g., "info", "warning", "error", "debug"). Case-insensitive.
            message: The log message content.
            component_name: The name of the framework component logging the message (e.g., "RequestRouter", "StateManager").
            traceId: Optional trace ID to correlate logs across operations.
            appId: Optional application ID context if the framework message is related to a specific app.
            requestId: Optional request ID context if the framework message is related to a specific request.
            metadata: Optional dictionary for additional context fields specific to this log entry.
        """
        # Get the logging level from the string, default to INFO if invalid
        log_level = getattr(logging, level.upper(), logging.INFO)

        # Prepare extra context for the JsonFormatter
        extra_context = {
            'component_name': component_name,
            'traceId': traceId,
            'appId': appId,
            'requestId': requestId,
            'metadata': metadata # Pass metadata to the formatter
        }
        # Filter out None values from extra_context before passing to avoid clutter
        extra_context = {k: v for k, v in extra_context.items() if v is not None}

        # Log the message using the configured logger
        self._logger.log(log_level, message, extra=extra_context)


    async def log_application_message(self, log_message: LogMessage):
        """
        Logs a structured message originating from an application sandbox.
        This method receives a LogMessage data model directly from the sandbox output.

        Args:
            log_message: The LogMessage object received from the application sandbox.
                         This object is expected to contain fields like level, message,
                         component_name, appId, requestId, taskId, context, and metadata.
        """
        # Get the logging level from the LogMessage object, default to INFO if invalid
        log_level = getattr(logging, log_message.level.upper(), logging.INFO)

        # Prepare extra context from the LogMessage data model for the JsonFormatter
        # The formatter is designed to pick up these fields from the 'extra' dict
        extra_context = {
            'component_name': log_message.component_name,
            'traceId': log_message.traceId,
            'appId': log_message.appId,
            'requestId': log_message.requestId,
            'taskId': log_message.taskId,
            'context': log_message.context,
            # Note: log_message.timestamp could be used, but the formatter uses record.created by default.
            # If the original application timestamp is critical, the formatter needs adjustment
            # or it should be included within the 'metadata' field.
            'metadata': log_message.metadata # Pass metadata from the LogMessage
        }
         # Filter out None values from extra_context before passing
        extra_context = {k: v for k, v in extra_context.items() if v is not None}

        # Log the message using the configured logger
        self._logger.log(log_level, log_message.message, extra=extra_context)


    # TODO: Add internal methods for configuring logging output (e.g., to file, remote endpoint) (Issue #XX)
    # TODO: Consider integrating with a dedicated logging backend (e.g., ELK stack, Loki) for production (Issue #XX)
    # TODO: Implement more sophisticated log processing or filtering if needed (Issue #XX)
