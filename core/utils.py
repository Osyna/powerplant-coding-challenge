from core.classes import Fuels, Powerplant
import yaml
import os


def get_config(default_path: str = 'config.yml'):
    """Get configuration from environment variables or config file"""
    # Load from config file first
    config = load_config(default_path)

    # Override with environment variables if they exist
    if os.getenv('DOCKER_ENV'):
        config['API'].update({
            'protocol': os.getenv('API_PROTOCOL', config['API']['protocol']),
            'host':     os.getenv('API_HOST', config['API']['host']),
            'port':     int(os.getenv('API_PORT', config['API']['port'])),
            'endpoint': os.getenv('API_ENDPOINT', config['API']['endpoint'])
            })
    return config


def load_config(default_path: str = 'config.yml'):
    """Load configuration from YAML file"""
    with open(default_path) as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Error loading config file: {exc}")
            exit(1)
    return config


def format_payload(payload):
    """Format the API payload into internal data structures"""
    print(payload)
    load = payload.load
    fuels_stat = Fuels(*payload.fuels.values())
    powerplants_list = [Powerplant(i + 1, **pw) for i, pw in enumerate(payload.powerplants)]
    return load, fuels_stat, powerplants_list