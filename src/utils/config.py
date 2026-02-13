"""Config loader"""
import yaml

def load_config():
    try:
        with open('config/config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except:
        return {}

CONFIG = load_config()
