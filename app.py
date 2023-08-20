from flask import *
import os
import json
import subprocess
import requests

app = Flask(__name__)
CONFIG_FILE = 'config.json'

def save_config(data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        initial_data = {
            "number_of_workers": 3,
            "average_delay": 1,
            "failure_percentage": 11
        }
        save_config(initial_data)
        return initial_data

# -----------------------------------------------LOAD BALANCER------------------------------------

class LoadBalancer:
    def __init__(self):
        self.server_process = None
        self.i = -1
        self.n = int(load_config()["number_of_workers"])

    def start_server(self):
        if not self.server_process:
            self.i = -1
            self.n = int(load_config()["number_of_workers"])
            self.server_process = subprocess.Popen(['python', 'workers.py'])
            print("worker servers started.")

    def stop_server(self):
        if self.server_process:
            self.server_process.kill()
            self.server_process.wait()
            self.server_process = None
            print("worker servers stopped.")


load_balancer = LoadBalancer()

def round_robin_worker_call(endpoint):
    load_balancer.i =  (load_balancer.i+1) % load_balancer.n
    url = f"http://127.0.0.1:{5000 + load_balancer.i}"+endpoint

    response = requests.get(url)
    api_response = Response(response.content, status=response.status_code)
    # Transfer headers from API response to Flask response
    for key, value in response.headers.items():
        api_response.headers[key] = value

    return api_response

@app.route('/api/v1/hello')
def hello():
    return round_robin_worker_call('/api/v1/hello')


@app.route('/worker/stats')
def worker_stats():
    return round_robin_worker_call('/worker/stats')



# -----------------------------------------------CONFIG MANAGER------------------------------------


@app.route("/")
def home():
    data = load_config()
    return render_template('home.html', data=data)


@app.route('/config', methods=['POST'])
def configChange():
    cur_data = load_config()
    a, b, c = request.form['workers'], request.form['delay'], request.form['failure_percentage']
    data = {
        "number_of_workers":  a if a != "" else cur_data["number_of_workers"],
        "average_delay":      b if b != "" else cur_data["average_delay"],
        "failure_percentage": c if c != "" else cur_data["failure_percentage"]
    }
    save_config(data)
    load_balancer.stop_server()
    load_balancer.start_server()
    return redirect("/")





# -----------------------------------------------MAIN------------------------------------
if __name__ == '__main__':
    load_balancer.start_server()
    app.run(port=3000)
    load_balancer.stop_server()
