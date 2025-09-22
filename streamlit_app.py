import streamlit as st
import paho.mqtt.client as mqtt

st.set_page_config(page_title="Siemens LOGO! Dashboard", layout="centered")
st.title("🚀 Siemens LOGO! Dashboard via MQTT")

q1_status = st.empty()
ai1_value = st.empty()

# Callback لما تجيلنا رسالة جديدة من MQTT
def on_message(client, userdata, msg):
    if msg.topic == "logo/q1":
        q1_status.markdown(f"**Q1 Status:** {'🟢 ON' if msg.payload.decode()=='ON' else '🔴 OFF'}")
    elif msg.topic == "logo/ai1":
        ai1_value.markdown(f"**AI1 Value:** {msg.payload.decode()}")

# MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("broker.hivemq.com", 1883, 60)
mqtt_client.subscribe("logo/#")
mqtt_client.loop_start()

st.info("📡 Connected to MQTT broker... waiting for data")
