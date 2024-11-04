import logging

logging.basicConfig(
    filename='activity.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_response(response):
    logging.info(f"Response: {response}")

def log_error(error):
    logging.error(f"Error: {error}")