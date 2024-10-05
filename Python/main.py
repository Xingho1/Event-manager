# import sqlConnection as scon
import pyscript as py
from pyscript import document 

def addevent():
    # tf.create_event(event_name = document.getElementById('ev-name-box').text)
    py.console.log( document.getElementById('ev-name-box').text)
