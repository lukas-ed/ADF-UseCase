import can
import datetime as dt

ev_ID = 0x101

bus = can.interface.Bus(interface='socketcan', channel='vcan0')

state = 0

def log_action(vnt):
    time_frame = dt.datetime.now().isoformat(timespec='auto')
    log_entry = {"Time": time_frame, "ECU": "BrakeLights ECU", "action": vnt}

    return log_entry

def brakelight_handler(sensor):
    global state
    if sensor == 1 and state != sensor:
        state = sensor
        vnt = "Lights On"
        log = log_action(vnt)
    elif sensor == 0 and state != sensor:
        state = sensor
        vnt = "Lights Off"
        log = log_action(vnt)
    else:
        print("invalid action")
        print("state=", state)
        return
    print("Action occured: \n", log, "\n")
    return

def main():
    #Since this is the lights.. i guess it only really needs recieving.. doesnt really need to send anything
    for msg in bus:
        if msg.arbitration_id == 0x100:
            light_state = msg.data[0]
            brakelight_handler(light_state)

if __name__ == "__main__":
    main()
    
    







    
