from flask import render_template

from Brownian import app
import elastibro.utils
import elastibro.errors

@app.route('/')
def home():
    name = "This is the home page."
    health, errors = elastibro.utils.getHealth()
    return render_template('home.html', name=name, health=health, errors=errors)

@app.route('/query')
def query():
    name = "This is the query page."
    health, errors = elastibro.utils.getHealth()
    return render_template('home.html', name=name, health=health, errors=errors)

@app.route('/notice')
def notices():
    name = "This is the notice page."
    health, errors = elastibro.utils.getHealth()
    return render_template('home.html', name=name, health=health, errors=errors)

@app.route('/health')
def health():
    health, errors = elastibro.utils.getHealth()
    nodes, errors = elastibro.utils.getNodeInfo(errors)
    shards, errors = elastibro.utils.getShardInfo(errors)
    return render_template('health.html', health=health, nodes=nodes, shards=shards, errors=errors)