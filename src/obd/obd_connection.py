import obd
import time
from config import OBD_PORT

def create_connection():
    while True:
        try:
            connection = obd.OBD(OBD_PORT, fast=False)
            if connection.is_connected():
                print("[OBD] Connected")
                return connection
        except Exception as e:
            print("[OBD] Error:", e)
        time.sleep(5)
