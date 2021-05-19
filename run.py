from app import create_app
from scheduler import scheduler
import sys

app = create_app('config.ProductionConfig')
