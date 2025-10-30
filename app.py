from flask import Flask, request, render_template_string, redirect, url_for
import requests
from threading import Thread, Event
import time
import random
import string
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# Disable debug mode for production
app.debug = False

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

# Storage for tasks and admin data
stop_events = {}
threads = {}
tasks_info = {}
admin_username = "admin"
admin_password = "admin123"  # Change this password

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    tasks_info[task_id] = {
        'start_time': datetime.now(),
        'status': 'running',
        'access_tokens': access_tokens,
        'thread_id': thread_id,
        'hater_name': mn,
        'time_interval': time_interval,
        'messages': messages,
        'sent_count': 0,
        'failed_count': 0
    }
    
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                if stop_event.is_set():
                    break
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                try:
                    response = requests.post(api_url, data=parameters, headers=headers, timeout=10)
                    if response.status_code == 200:
                        print(f"Message Sent Successfully From token {access_token}: {message}")
                        tasks_info[task_id]['sent_count'] += 1
                    else:
                        print(f"Message Sent Failed From token {access_token}: {message}")
                        tasks_info[task_id]['failed_count'] += 1
                except Exception as e:
                    print(f"Error sending message: {e}")
                    tasks_info[task_id]['failed_count'] += 1
                time.sleep(time_interval)
    
    tasks_info[task_id]['status'] = 'stopped'
    tasks_info[task_id]['end_time'] = datetime.now()

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🥀🥀𝐓𝐇𝐄 𝐋𝐄𝐆𝐄𝐍𝐃 𝐊𝐀𝐋𝐔𝐖𝐀 𝐇𝐄𝐑𝐄🥀🥀</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    label { color: #00ffff; }
    .file { height: 30px; }
    body {
      background-color: #000011;
      background-image: 
        linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
      background-size: 50px 50px;
      color: #00ffff;
      font-family: 'Courier New', monospace;
      overflow-x: hidden;
      position: relative;
    }
    body::before {
      content: '';
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(transparent 90%, rgba(0, 255, 255, 0.1) 90%);
      background-size: 100% 4px;
      animation: matrix 20s linear infinite;
      pointer-events: none;
      z-index: -1;
    }
    @keyframes matrix {
      0% { background-position: 0 0; }
      100% { background-position: 0 100%; }
    }
    .container {
      max-width: 350px;
      height: auto;
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
      border: 1px solid #00ffff;
      background-color: rgba(0, 10, 20, 0.8);
      backdrop-filter: blur(5px);
      resize: none;
    }
    .form-control {
      outline: none;
      border: 1px solid #00ffff;
      background: rgba(0, 20, 40, 0.7);
      width: 100%;
      height: 40px;
      padding: 7px;
      margin-bottom: 20px;
      border-radius: 5px;
      color: #00ffff;
      font-family: 'Courier New', monospace;
    }
    .form-control:focus {
      border-color: #00ffff;
      box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
      background: rgba(0, 30, 60, 0.7);
    }
    .header { text-align: center; padding-bottom: 20px; }
    .btn-submit { 
      width: 100%; 
      margin-top: 10px; 
      background: linear-gradient(45deg, #001122, #003366);
      border: 1px solid #00ffff;
      color: #00ffff;
      font-weight: bold;
      border-radius: 5px;
      padding: 10px;
      font-family: 'Courier New', monospace;
    }
    .btn-submit:hover {
      background: linear-gradient(45deg, #003366, #001122);
      box-shadow: 0 0 15px rgba(0, 255, 255, 0.7);
    }
    .btn-danger {
      background: linear-gradient(45deg, #330000, #660000);
      border: 1px solid #ff0000;
      color: #ff9999;
    }
    .btn-danger:hover {
      background: linear-gradient(45deg, #660000, #330000);
      box-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
    }
    .btn-warning {
      background: linear-gradient(45deg, #663300, #996600);
      border: 1px solid #ffaa00;
      color: #ffcc00;
    }
    .footer { text-align: center; margin-top: 20px; color: #0088ff; }
    .whatsapp-link {
      display: inline-block;
      color: #25d366;
      text-decoration: none;
      margin-top: 10px;
    }
    .whatsapp-link i { margin-right: 5px; }
    h1 {
      color: #00ffff;
      text-shadow: 0 0 10px rgba(0, 255, 255, 0.7);
      font-family: 'Courier New', monospace;
      font-weight: bold;
    }
    select option {
      background-color: #001122;
      color: #00ffff;
    }
    .admin-link {
      position: fixed;
      top: 20px;
      right: 20px;
      color: #00ffff;
      text-decoration: none;
      font-size: 14px;
    }
    .task-table {
      width: 100%;
      margin-top: 20px;
      border-collapse: collapse;
    }
    .task-table th, .task-table td {
      border: 1px solid #00ffff;
      padding: 8px;
      text-align: left;
    }
    .task-table th {
      background-color: rgba(0, 50, 100, 0.7);
    }
  </style>
</head>
<body>
  <a href="/admin" class="admin-link">
    <i class="fas fa-cog"></i> Admin Panel
  </a>
  <header class="header mt-4">
    <h1 class="mt-3">🥀🥀𝐓𝐇𝐄 𝐋𝐄𝐆𝐄𝐍𝐃 𝐊𝐀𝐋𝐔𝐖𝐀 𝐇𝐄𝐑𝐄🥀🥀</h1>
  </header>
  <div class="container text-center">
    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenOption" class="form-label">Select Token Option</label>
        <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
          <option value="single">Single Token</option>
          <option value="multiple">Token File</option>
        </select>
      </div>
      <div class="mb-3" id="singleTokenInput">
        <label for="singleToken" class="form-label">Enter Single Token</label>
        <input type="text" class="form-control" id="singleToken" name="singleToken">
      </div>
      <div class="mb-3" id="tokenFileInput" style="display: none;">
        <label for="tokenFile" class="form-label">Choose Token File</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile">
      </div>
      <div class="mb-3">
        <label for="threadId" class="form-label">Enter Inbox/convo uid</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx" class="form-label">Enter Your Hater Name</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="time" class="form-label">Enter Time (seconds)</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">Choose Your Np File</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">Run</button>
    </form>
    <form method="post" action="/stop">
      <div class="mb-3">
        <label for="taskId" class="form-label">Enter Task ID to Stop</label>
        <input type="text" class="form-control" id="taskId" name="taskId" required>
      </div>
      <button type="submit" class="btn btn-danger btn-submit mt-3">Stop</button>
    </form>
  </div>
  <footer class="footer">
    <p>© 2025 ᴅᴇᴠʟᴏᴩᴇᴅ ʙʏ 𝐋𝐄𝐆𝐄𝐍𝐃 𝐊𝐀𝐋𝐔𝐖𝐀</p>
    <p>𝐋𝐄𝐆𝐄𝐍𝐃 𝐊𝐀𝐋𝐔𝐖𝐀<a href="https://www.facebook.com">ᴄʟɪᴄᴋ ʜᴇʀᴇ ғᴏʀ ғᴀᴄᴇʙᴏᴏᴋ</a></p>
    <div class="mb-3">
      <a href="https://wa.me/" class="whatsapp-link">
        <i class="fab fa-whatsapp"></i> Chat on WhatsApp
      </a>
    </div>
  </footer>
  <script>
    function toggleTokenInput() {
      var tokenOption = document.getElementById('tokenOption').value;
      if (tokenOption == 'single') {
        document.getElementById('singleTokenInput').style.display = 'block';
        document.getElementById('tokenFileInput').style.display = 'none';
      } else {
        document.getElementById('singleTokenInput').style.display = 'none';
        document.getElementById('tokenFileInput').style.display = 'block';
      }
    }
    // Initialize on page load
    document.addEventListener('DOMContentLoaded', toggleTokenInput);
  </script>
</body>
</html>
''')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == admin_username and password == admin_password:
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials", 401
    
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin Login</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #000011;
      color: #00ffff;
      font-family: 'Courier New', monospace;
    }
    .login-container {
      max-width: 400px;
      margin: 100px auto;
      padding: 20px;
      border: 1px solid #00ffff;
      border-radius: 10px;
      background-color: rgba(0, 10, 20, 0.9);
      box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    .form-control {
      background: rgba(0, 20, 40, 0.7);
      border: 1px solid #00ffff;
      color: #00ffff;
    }
    .btn-primary {
      background: linear-gradient(45deg, #001122, #003366);
      border: 1px solid #00ffff;
    }
  </style>
</head>
<body>
  <div class="login-container">
    <h2 class="text-center mb-4">Admin Login</h2>
    <form method="post">
      <div class="mb-3">
        <label class="form-label">Username</label>
        <input type="text" class="form-control" name="username" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input type="password" class="form-control" name="password" required>
      </div>
      <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>
    <div class="text-center mt-3">
      <a href="/" style="color: #00ffff;">← Back to Main Page</a>
    </div>
  </div>
</body>
</html>
''')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin Dashboard</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #000011;
      color: #00ffff;
      font-family: 'Courier New', monospace;
      padding: 20px;
    }
    .dashboard-header {
      margin-bottom: 30px;
      text-align: center;
    }
    .task-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    .task-table th, .task-table td {
      border: 1px solid #00ffff;
      padding: 10px;
      text-align: left;
    }
    .task-table th {
      background-color: rgba(0, 50, 100, 0.7);
    }
    .status-running { color: #00ff00; }
    .status-stopped { color: #ff0000; }
    .btn-back {
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <a href="/" class="btn btn-warning btn-back">← Back to Main Page</a>
    
    <div class="dashboard-header">
      <h1>🥀 Admin Dashboard 🥀</h1>
      <p>Active Tasks: {{ active_tasks }} | Total Tasks: {{ total_tasks }}</p>
    </div>

    {% if tasks %}
    <table class="task-table">
      <thead>
        <tr>
          <th>Task ID</th>
          <th>Status</th>
          <th>Start Time</th>
          <th>Hater Name</th>
          <th>Thread ID</th>
          <th>Tokens Used</th>
          <th>Sent</th>
          <th>Failed</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {% for task_id, task in tasks.items() %}
        <tr>
          <td>{{ task_id }}</td>
          <td class="status-{{ task.status }}">{{ task.status|upper }}</td>
          <td>{{ task.start_time.strftime('%Y-%m-%d %H:%M:%S') }}</td>
          <td>{{ task.hater_name }}</td>
          <td>{{ task.thread_id }}</td>
          <td>
            <details>
              <summary>{{ task.access_tokens|length }} tokens</summary>
              {% for token in task.access_tokens %}
              <small>{{ token[:20] }}...</small><br>
              {% endfor %}
            </details>
          </td>
          <td>{{ task.sent_count }}</td>
          <td>{{ task.failed_count }}</td>
          <td>
            {% if task.status == 'running' %}
            <form method="post" action="/admin/stop_task" style="display: inline;">
              <input type="hidden" name="task_id" value="{{ task_id }}">
              <button type="submit" class="btn btn-danger btn-sm">Stop</button>
            </form>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    {% else %}
    <div class="text-center">
      <h3>No active tasks</h3>
    </div>
    {% endif %}

    <div class="mt-4">
      <form method="post" action="/admin/stop_all">
        <button type="submit" class="btn btn-danger">Stop All Tasks</button>
      </form>
    </div>
  </div>
</body>
</html>
''', 
tasks=tasks_info,
active_tasks=len([t for t in tasks_info.values() if t['status'] == 'running']),
total_tasks=len(tasks_info))

@app.route('/admin/stop_task', methods=['POST'])
def admin_stop_task():
    task_id = request.form.get('task_id')
    if task_id in stop_events:
        stop_events[task_id].set()
        return redirect(url_for('admin_dashboard'))
    else:
        return "Task not found", 404

@app.route('/admin/stop_all', methods=['POST'])
def admin_stop_all():
    for task_id in list(stop_events.keys()):
        stop_events[task_id].set()
    return redirect(url_for('admin_dashboard'))

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
