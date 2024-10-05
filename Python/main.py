# import sqlConnection as scon
import pyscript as py
from pyscript import document 
def addevent(event):
    # tf.create_event(event_name = document.getElementById('ev-name-box').text)
    
    intxt = document.querySelector("#ev-name-box").value
    document.querySelector(".ev-name").innerHTML = intxt