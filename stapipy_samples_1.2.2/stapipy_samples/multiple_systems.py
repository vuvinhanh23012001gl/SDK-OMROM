"""
 This sample shows how to use multiple GenTL modules (cti files) for acquiring image data.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to the first detected camera of all system
 - Acquire image data (with waiting in main thread) 
 - Use multiple GenTL module.
"""

import stapipy as st

# Number of images to grab
number_of_images_to_grab = 100

try:
    # Initialize StApi before using.
    st.initialize()

    # Create a system object list for store system object.
    # Then we try to create objects of all available systems.
    system_list = st.PyStSystemList()

    for system_vendor in st.EStSystemVendor:
        if system_vendor == st.EStSystemVendor.Count:
            continue
        try:
            # For each available system, 
            # try to create object for it then register it into system list for further usage.
            system_list.register(st.create_system(system_vendor, st.EStInterfaceType.All))
        except st.PyStError as st_error:
            print("An exception occurred.", st_error)

    # Create a device object of the first detected device to connect.
    st_device = system_list.create_first_device(st.ETLDeviceAccessFlags.AccessExclusive)

    # Display DisplayName of the device.
    print('Device=', st_device.info.display_name)

    # Create a datastream object for handling image stream data.
    st_datastream = st_device.create_datastream(0)

    # Start the image acquisition of the host side.
    st_datastream.start_acquisition(number_of_images_to_grab)

    # Start the image acquisition of the camera side.
    st_device.acquisition_start()

    # A while loop for acquiring data and checking status
    while st_datastream.is_grabbing:
        # Retrieve the buffer of image data with a timeout of 5000ms.
        with st_datastream.retrieve_buffer(5000) as st_buffer:
            # Check if the acquired data contains image data.
            if st_buffer.info.is_image_present:
                # Create an image object.
                st_image = st_buffer.get_image()
                # Display the information of the acquired image data.
                print("BlockID={0} Size={1} x {2} First Byte={3}".format(
                      st_buffer.info.frame_id,
                      st_image.width, st_image.height,
                      st_image.get_image_data()[0]))
            else:
                # If the acquired data contains no image data.
                print("Image data does not exist.")

    # Stop the image acquisition of the camera side
    st_device.acquisition_stop()

    # Stop the image acquisition of the host side
    st_datastream.stop_acquisition()

except Exception as exception:
    print(exception)
finally:
    input("Press enter to terminate")
