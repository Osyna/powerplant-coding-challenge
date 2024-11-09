import uvicorn
from core.api import productionApp
from core.utils import load_config

config = load_config('config.yml')

uvicorn.run(productionApp, host=config['API']['host'], port=config['API']['port'])



