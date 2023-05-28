from src.services.config_service import ConfigService
from src.services.data_service import DataService

from src.utils.globals import Globals

from flask import request, render_template
from flask.views import MethodView

####################################################################
from apscheduler.schedulers.background import BackgroundScheduler
count = 1
def update_counter():
    global count 
    count += 1
    Globals.socketio.emit("update_counter", {'count': count})
counter_scheduler = BackgroundScheduler()
counter_scheduler.add_job(update_counter, trigger="cron", second="*/5")
counter_scheduler.start()
####################################################################

class MainController(MethodView):
    init_every_request= False
    
    def __init__(self, config_service: ConfigService, data_service: DataService):
        self.config_service = config_service
        self.data_service = data_service
        
    def get(self):
        global count
        return render_template("main.html", count=count)