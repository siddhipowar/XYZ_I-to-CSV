import cv2
import numpy as np
import chronoptics.tof as tof
import time
import csv

# Initialize 3D camera
serial = "202004d"
cam = tof.KeaCamera(serial=serial)
tof.selectStreams(cam, [tof.FrameType.Z, tof.FrameType.INTENSITY, tof.FrameType.XYZ])
cam.start()

time.sleep(1)
config = cam.getCameraConfig()
config.reset()
time.sleep(1)
config.setIntegrationTime(0, [50, 50, 50, 50])
cam.setCameraConfig(config)

time.sleep(2)

# Global variables
draw = False  # True if the mouse is pressed. Used for selecting ROI.
roi_selected = False  # Flag to check if ROI has been selected
rect = (0, 0, 0, 0)  # Coordinates of the rectangle (ROI)
start_point = (0, 0)  # Starting point of the rectangle

# Mouse callback function for selecting ROI
def click_event(event, x, y, flags, param):
    global start_point, draw, rect, roi_selected, frame

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        draw = True
        roi_selected = False

    elif event == cv2.EVENT_MOUSEMOVE and draw:
        end_point = (x, y)
        temp_frame = frame.copy()
        cv2.rectangle(temp_frame, start_point, end_point, (0, 255, 0), 1)
        cv2.imshow("Frame", temp_frame)

    elif event == cv2.EVENT_LBUTTONUP:
        draw = False
        roi_selected = True
        rect = (start_point[0], start_point[1], x, y)
        cv2.rectangle(frame, start_point, (x, y), (0, 255, 0), 2)
        cv2.imshow("Frame", frame)

# Capture one frame to display
frames = cam.getFrames()
depth_frame = np.asarray(frames[1], dtype=np.float32)
intensity_frame = np.asarray(frames[0])
xyz_frame = np.asarray(frames[2])

# Convert depth to a visual format for display
depth_visual = cv2.normalize(depth_frame, None, 0, 255, cv2.NORM_MINMAX)
depth_visual = depth_visual.astype(np.uint8)

# Apply color map to the normalized depth image
colored_depth = cv2.applyColorMap(depth_visual, cv2.COLORMAP_JET)

frame = colored_depth
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_event)
cv2.imshow("Frame", frame)

# Wait until ROI is selected
while not roi_selected:
    cv2.waitKey(1)

x1, y1, x2, y2 = rect
cropped_intensity = intensity_frame[y1:y2, x1:x2]
print("Cropped intensity frame", cropped_intensity.shape)

cropped_xyz = xyz_frame[y1:y2, x1:x2]
print("xyz frame:", cropped_xyz.shape)

cropped_xyz_flat = cropped_xyz.reshape(-1, 4)[:,:3]  # Take only x, y, z, discard padding
cropped_intensity_flat = cropped_intensity.flatten()

combined_data = np.column_stack((cropped_xyz_flat, cropped_intensity_flat))

csv_file_path = "50us_output.csv"
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['X', 'Y', 'Z', 'Intensity'])
    for row in combined_data:
        writer.writerow(row)

print(f"Data saved to {csv_file_path}")

time.sleep(1)
config = cam.getCameraConfig()
config.reset()
time.sleep(1)
config.setIntegrationTime(0, [1000, 1000, 1000, 1000])
cam.setCameraConfig(config)

time.sleep(2)

frames = cam.getFrames()
depth_frame_long = np.asarray(frames[1], dtype=np.float32)
intensity_frame_long = np.asarray(frames[0])
xyz_frame_long = np.asarray(frames[2])

cropped_intensity_long = intensity_frame_long[y1:y2, x1:x2]
print("Cropped intensity frame", cropped_intensity.shape)

cropped_xyz_long = xyz_frame_long[y1:y2, x1:x2]
print("xyz frame:", cropped_xyz.shape)

cropped_xyz_flat_long = cropped_xyz_long.reshape(-1, 4)[:,:3]  # Take only x, y, z, discard padding
cropped_intensity_flat_long = cropped_intensity_long.flatten()

combined_data_long = np.column_stack((cropped_xyz_flat_long, cropped_intensity_flat_long))

csv_file_path = "1000us_output.csv"
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['X', 'Y', 'Z', 'Intensity'])
    for row in combined_data_long:
        writer.writerow(row)

print(f"Data saved to {csv_file_path}")


# Cleanup
cam.stop()
cv2.destroyAllWindows()
