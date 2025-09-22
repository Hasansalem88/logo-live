from pyModbusTCP.client import ModbusClient
import paho.mqtt.client as mqtt
import time

# 🟢 Connect to LOGO! PLC
plc = ModbusClient(host="192.168.0.100", port=502, auto_open=True)  # عدّل الـ IP بتاع LOGO!

# 🟢 Connect to public MQTT broker
mqtt_client = mqtt.Client()
mqtt_client.connect("broker.hivemq.com", 1883, 60)

while True:
    try:
        # قراءة Coil (مثلاً Q1 = أول Output)
        q1 = plc.read_coils(1, 1)
        if q1:
            mqtt_client.publish("logo/q1", "ON" if q1[0] else "OFF")

        # قراءة Analog Input (AI1 = أول مدخل تناظري)
        ai1 = plc.read_input_registers(0, 1)
        if ai1:
            mqtt_client.publish("logo/ai1", str(ai1[0]))

        print("✅ Published Q1 + AI1 to MQTT broker")
        time.sleep(2)

    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(5)
