import time
from can import interface, Notifier, BufferedReader, Message, CanError

import copy

config = {
'interface': 'vector',
'channel': 0,
'bit_rate': 500000,
'data_rate': 2000000,
'app_name': 'test',
'app_channel': 0,
}

def _print_msg(data):
	print(f'Recieved msg : {data}')

can_bus = interface.Bus(interface=config['interface'],
                        channel=config['channel'],
                        bitrate=config['bit_rate'],
                        data_bitrate=config['data_rate'],
                        app_name=config['app_name'],
                        app_channel=config['app_channel'],
                        sjw_abr = 2,
                        tseg1_abr = 55,
                        tseg2_abr= 24,
                        sjw_dbr = 10,
                        tseg1_dbr = 29,
                        tseg2_dbr = 10,
                        fd=True
                        )
rx_buffer = BufferedReader()
can_notifier = Notifier(can_bus, [_print_msg, rx_buffer])

id = 0x222	# temp id
msg = Message(arbitration_id=id,
                data=[0xFF, 0xFF, 0xFF],
                channel=0,
                is_rx=False,
                is_extended_id=False
                )

print(msg)
print("Success: CONNECT CAN DEVICE")

try:
    while True:
        received_msg = rx_buffer.get_message(timeout=0.05)
        if received_msg is not None:
            print(f"Received message from buffer: \n {received_msg}")
        else:
            print("No message received from buffer")
        can_bus.send(msg)

except CanError as e:
    print(f"Error: {e}")
    print("Error: Failed to send message")
