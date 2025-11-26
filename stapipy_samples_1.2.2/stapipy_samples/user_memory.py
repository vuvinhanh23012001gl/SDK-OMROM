"""
 This sample shows how to use UserMemory function.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - How to read user data from the rom and to write user data to the rom.
"""

import stapipy as st

# Feature names
DEVICE_USER_MEMORY = "DeviceUserMemory"

def display_register(register_node):
    buffer = register_node.value
    for i, val in enumerate(buffer):
        if (i & 0xF) == 0:
            print("{0:04X}\t".format(i), end='')
        print("{0:02X} ".format(val), end='')
        if (i & 0xF) == 0xF:
            print("")
    print("")

if __name__ == "__main__":
    try:
        # Initialize StApi before using.
        st.initialize()

        # Create a system object for device scan and connection.
        st_system = st.create_system()

        # Connect to first detected device.
        st_device = st_system.create_first_device(
            st.ETLDeviceAccessFlags.AccessExclusive)

        # Display DisplayName of the device.
        print('Device=', st_device.info.display_name)

        # Get the remote nodemap.
        nodemap = st_device.remote_port.nodemap

        # Use NodeMap object to access current setting of the camera.
        node_user_memory = nodemap.get_node(DEVICE_USER_MEMORY)

        if node_user_memory:
            display_register(node_user_memory.get())
        else:
            print(DEVICE_USER_MEMORY + " is not supported by this camera.")

    except Exception as exception:
        print(exception)
