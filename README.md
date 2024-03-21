# XYZ_I-to-CSV

This program allows to select a ROI and outputs CSV files of 50us and 1000us integration time frames. It outputs CSV file of the format X, Y, Z, and Intensity columns of both 50us and 1000us frames each, of selected area.

Algorithm:
* Initialize the camera with the serial number and set frame types to XYZ, Intensity
* set integration time to 50us
* capture frames and convert it to arrays
* Display frames using OpenCV for ROI selection. Mouse callback function ‘click_event’ handles selection of ROI and stores coordinates of the selected region
* Once the region is selected, XYZ and intensity frames are cropped. They are combined to form 4 columns of X, Y, Z and Intensity and columns are written to CSV files.
* Output is stored in ‘50us_ouput.csv’
* Same process is repeated for 1000us integration time frames. Output is stored in ‘1000us_output.csv’
