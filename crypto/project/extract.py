import requests
from decouple import config, Csv

coins = config('COINS',default='xrp-xrp',cast=Csv())