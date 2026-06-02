from flask import Flask
from redis import Redis
from healthcheck import HealthCheck
import os

app = Flask(__name__)

redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True) # En docker compose reemplazar "localhost" por "redis"
# Healthckech ---------
health = HealthCheck()
def redis_available():
    info = redis_client.info()
    return True, "redis ok"
health.add_check(redis_available)
app.add_url_rule("/hc", "healthcheck", view_func=lambda: health.run())

@app.route('/')
def hello():
    count = redis_client.incr('hits')
    msg = '¡Hola gente! Me han visitado {} veces.\n'.format(count)
    print(msg)
    return msg

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)