import logging
import os
from datetime import datetime
from config import LOG_LEVEL, LOG_FILE

def initialize_logger(logger_name="logistics_dashboard"):

    os.makedirs("logs", exist_ok=True)

    log = logging.getLogger(logger_name)
    log.setLevel(getattr(logging, LOG_LEVEL.upper()))
    log.handlers.clear()

    format_pattern = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )

    file_output = logging.FileHandler(f"logs/{LOG_FILE}")
    file_output.setLevel(logging.INFO)
    file_output.setFormatter(format_pattern)

    stream_output = logging.StreamHandler()
    stream_output.setLevel(logging.INFO)
    stream_output.setFormatter(format_pattern)

    log.addHandler(file_output)
    log.addHandler(stream_output)

    return log

def record_pipeline_event(event_name, state="INITIATED", info=None):
    logger = initialize_logger()
    log_msg = f"Event: {event_name} | Status: {state}"
    if info:
        log_msg += f" | Info: {info}"

    if state == "INITIATED":
        logger.info(log_msg)
    elif state == "FINISHED":
        logger.info(log_msg)
    elif state == "FAILED":
        logger.error(log_msg)
    elif state == "WARNING":
        logger.warning(log_msg)

    return logger

def record_data_validation(validation_name, outcome, notes=None):
    logger = initialize_logger()
    log_msg = f"Validation: {validation_name} | Outcome: {outcome}"
    if notes:
        log_msg += f" | Notes: {notes}"

    if outcome == "PASS":
        logger.info(log_msg)
    elif outcome == "FAIL":
        logger.error(log_msg)
    elif outcome == "WARNING":
        logger.warning(log_msg)

    return logger

def generate_alert(alert_name, description, level="INFO"):
    logger = initialize_logger()
    alert_text = f"ALERT [{alert_name}]: {description}"

    if level == "CRITICAL":
        logger.critical(alert_text)
    elif level == "ERROR":
        logger.error(alert_text)
    elif level == "WARNING":
        logger.warning(alert_text)
    else:
        logger.info(alert_text)

    return logger
