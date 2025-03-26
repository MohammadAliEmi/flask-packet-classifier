from flask import Flask, render_template, jsonify
from scapy.all import sniff
from threading import Thread
import json

app = Flask(__name__)
packet_data = []

def capture_packets():
    def process_packet(packet):
        protocol = packet.sprintf("%IP.proto%")
        src_ip = packet.sprintf("%IP.src%")
        dst_ip = packet.sprintf("%IP.dst%")
        src_port = packet.sprintf("%IP.sport%")
        dst_port = packet.sprintf("%IP.dport%")
        packet_info = {
            "protocol": protocol,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": src_port,
            "dst_port": dst_port
        }
        packet_data.append(packet_info)

    sniff(prn=process_packet, store=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_capture')
def start_capture():
    capture_thread = Thread(target=capture_packets)
    capture_thread.start()
    return jsonify({"status": "capture started"})

@app.route('/get_packets')
def get_packets():
    return jsonify(packet_data)

if __name__ == '__main__':
    app.run(debug=True)
