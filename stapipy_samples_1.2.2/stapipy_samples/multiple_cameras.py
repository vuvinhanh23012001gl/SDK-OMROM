"""
 This sample shows how to conect and get images from all available cameras.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to all available cameras
 - Acquire image from the list of camera
 You can see how to handle multiple cameras/stream objects in this sample.
"""

import stapipy as st

# Number of images to grab
number_of_images_to_grab = 10

try:
    # Initialize StApi before using.
    st.initialize()

    # Create a system object for device scan and connection.
    st_system = st.create_system()

    # Create a camera device list object to store all the cameras.
    device_list = st.PyStDeviceList()

    # Create a DataStream list object to store all the data stream object related to the cameras.
    stream_list = st.PyStDataStreamList()

    while True:
        try:
            st_device = st_system.create_first_device()
        except:
            if not device_list:
                raise
            break
        # Add the camera into device object list for later usage.
        device_list.register(st_device)

        # Display the DisplayName of the device.
        print("Device {0} = {1}".format(len(device_list), st_device.info.display_name))

        # Create a DataStream object then add into DataStream list for later usage.
        stream_list.register(st_device.create_datastream(0))

    # Start the image acquisition of the host side.
    stream_list.start_acquisition(number_of_images_to_grab)

    # Start the image acquisition of the camera side.
    device_list.acquisition_start()

    # Loop for aquiring data and checking status
    while stream_list.is_grabbing_any:
        # Retrieve data buffer of image data from any camera with a timeout of 5000ms.
        with stream_list.retrieve_buffer(5000) as st_buffer:
            # Check if the acquired data contains image data.
            if st_buffer.info.is_image_present:
                print("{0} : BlockID={1} {2:.2f}FPS"\
                    .format(st_buffer.datastream.device.info.display_name,
                            st_buffer.info.frame_id,
                            st_buffer.datastream.current_fps))
            else:
                print("Image data does not exist.")

    # Stop the image acquisition of the camera side.
    device_list.acquisition_stop()

    # Stop the image acquisition of the host side.
    stream_list.stop_acquisition()

except Exception as exception:
    print(exception)
finally:
    input("Press enter to terminate")
