from flask import Flask, render_template, jsonify, send_file
from flask_socketio import SocketIO, emit
import time
import pandas as pd
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Giả lập trạng thái máy bơm
pump_status = [False] * 10  # Tất cả máy bơm đều tắt
pump_start_time = [0] * 10   # Thời gian bắt đầu bật máy bơm
pump_time_on = [0] * 10       # Thời gian bật của từng máy bơm
log_data = []  # Danh sách lưu trữ nhật ký hoạt động

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/export')
def export_data():
    # Tạo DataFrame từ log_data
    df = pd.DataFrame(log_data, columns=['Thời Gian', 'Máy Bơm', 'Trạng Thái'])
    
    # Lưu DataFrame vào file Excel
    file_name = f'pump_log_{datetime.now().strftime("%Y%m%d")}.xlsx'
    df.to_excel(file_name, index=False)

    # Trả về file Excel cho người dùng
    return send_file(file_name, as_attachment=True)

@socketio.on('toggle_pump')
def toggle_pump(pump_id):
    if 0 <= pump_id < 10:
        if not pump_status[pump_id]:  # Nếu máy bơm tắt
            pump_start_time[pump_id] = time.time()  # Ghi nhận thời gian bật
            log_data.append((datetime.now(), pump_id + 1, "Bật"))  # Ghi lại vào log
        else:  # Nếu máy bơm bật
            pump_time_on[pump_id] += time.time() - pump_start_time[pump_id]  # Cập nhật thời gian bật
            log_data.append((datetime.now(), pump_id + 1, "Tắt"))  # Ghi lại vào log

        pump_status[pump_id] = not pump_status[pump_id]  # Đổi trạng thái máy bơm
        
        status = "Bật" if pump_status[pump_id] else "Tắt"
        print(f"Máy bơm {pump_id + 1} đã {status}. Thời gian bật: {pump_time_on[pump_id]:.2f} giây.")

        # Gửi trạng thái và thời gian bật đến client
        emit('update_status', {'status': pump_status, 'time_on': pump_time_on}, broadcast=True)

@socketio.on('get_status')
def get_status():
    emit('update_status', {'status': pump_status, 'time_on': pump_time_on})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
