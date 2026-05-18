import can
import datetime as dt

ev_ID = 0x100
state = 0
bus = can.interface.Bus(interface='socketcan', channel='vcan0')

def log_action(vnt, vnt_desc):
    time_frame = dt.datetime.now().isoformat(timespec='auto')
    log_entry = {"Time": time_frame, "ECU": "Brake ECU", "action": vnt, "description": vnt_desc}

    return log_entry


def brake_event_handler(sensor):
    
    global state

    if sensor == 1 and state != sensor:
        state = sensor
        vnt_desc = "Brake Engaged"
        bus_msg(state)
        log = log_action(state, vnt_desc)
    elif sensor == 0 and state != sensor:
        state = sensor
        vnt_desc = "Brake Disengage"
        bus_msg(state)
        log = log_action(state, vnt_desc)
    else:
        print("invalid action")
        print("state=", state)
        return
    print("Action occured: \n", log, "\n")
    return

def bus_msg(event):
    msg = can.Message(
        arbitration_id=ev_ID, 
        data = [event],
        is_extended_id=True
    )
    try:
        bus.send(msg)
        print(f'Message channel {bus.channel_info}')
    except can.CanError:
        log = log_action("CAN SEND Error")
        print(f'Message failed:\n{log}')

def main():
    while True:
        pre_conv = input("Breakpedal\n")
        try:
            sensor = int(pre_conv)
        except ValueError:
            print("Error: Please enter a valid number (1 or 0).\n")
            continue
        
        brake_event_handler(sensor)

if __name__ == "__main__":
    main()







