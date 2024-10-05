# import sqlConnection as scon
import pyscript as py
from pyscript import document 
from pyscript import console
def addevent(event):
    # tf.create_event(event_name = document.getElementById('ev-name-box').text)
    out = document.getElementByClassName('ev-name')

    out.innerHTML = document.getElementById('ev-name-box').innerHTML
