# import the necessary packages
from pyimagesearch.tempimage import TempImage
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
import copy
class CameraHandler():
    def __init__(self, ConfigPointer):
        self.ConfigPointer = ConfigPointer
    def ConfigureCamera(self, conf):
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = tuple(self.ConfigPointer["resolution"])
        camera.framerate = self.ConfigPointer["fps"]
        rawCapture = PiRGBArray(camera, size=tuple(self.ConfigPointer["resolution"]))
        
        # allow the camera to warmup, then initialize the average frame, last
        # uploaded timestamp, and frame motion counter
        print "[INFO] warming up..."
        time.sleep(self.ConfigPointer["camera_warmup_time"])
        return camera, rawCapture
    def ConnectToDropbox(self):
        from dropbox.client import DropboxOAuth2FlowNoRedirect
        from dropbox.client import DropboxClient
    
        # connect to dropbox and start the session authorization process
        flow = DropboxOAuth2FlowNoRedirect(conf["dropbox_key"], conf["dropbox_secret"])
        print "[INFO] Authorize this application: {}".format(flow.start())
        authCode = raw_input("Enter auth code here: ").strip()

        # finish the authorization and grab the Dropbox client
        (accessToken, userID) = flow.finish(authCode)
        client = DropboxClient(accessToken)
        print "[SUCCESS] dropbox account linked"
        return client
    def CaptureN(self, f):
        # resize the frame, convert it to grayscale, and blur it
        frame = f.array
        frame = imutils.resize(frame, width=200)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return frame, gray
    
    def main():
        conf = GetConfig()
        
        if conf["use_dropbox"]:
            client = ConnectToDropbox()
        
        camera, rawCapture = ConfigureCamera(conf)
        
        lastUploaded = datetime.datetime.now()
        motionCounter = 0
        
        camera.capture(rawCapture, format="bgr", use_video_port=True)
        frame, gray = CaptureN(rawCapture)
        avg = gray.copy().astype("float")
        rawCapture.truncate(0)
        
        # capture frames from the camera
        for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            frame, gray = CaptureN(f)
        
            # accumulate the weighted average between the current frame and
            # previous frames, then compute the difference between the current
            # frame and running average
            cv2.accumulateWeighted(gray, avg, 0.5)
            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
            
            # threshold the delta image, dilate the thresholded image to fill
            # in holes, then find contours on thresholded image
            thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) >= conf["min_area"]:
                    # compute the bounding box for the contour, draw it on the frame,
                    # and update the text
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # check to see if the room is occupied
                    motionCounter += 1
        
            # check to see if the number of frames with consistent motion is
            # high enough
            if motionCounter >= conf["min_motion_frames"]:
                # draw the text and timestamp on the frame
                timestamp = datetime.datetime.now()
                ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
                cv2.putText(frame, "Room Status: {}".format("Occupied"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)    
                    
                # check to see if dropbox sohuld be used
                if conf["use_dropbox"] and (datetime.datetime.now() - lastUploaded).seconds >= conf["min_upload_seconds"]:
                    # write the image to temporary file
                    t = TempImage()
                    cv2.imwrite(t.path, frame)
        
                    # upload the image to Dropbox and cleanup the tempory image
                    print "[UPLOAD] {}".format(ts)
                    path = "{base_path}/{timestamp}.jpg".format(base_path=conf["dropbox_base_path"], timestamp=ts)
                    client.put_file(path, open(t.path, "rb"))
                    t.cleanup()
        
                    # update the last uploaded timestamp and reset the motion counter
                    lastUploaded = timestamp
                motionCounter = 0
            # check to see if the frames should be displayed to screen
            if conf["show_video"]:
                # display the security feed
                cv2.imshow("Security Feed", frame)
                key = cv2.waitKey(1) & 0xFF
        
                # if the `q` key is pressed, break from the loop
                if key == ord("q"):
                    break
        
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
        






if __name__ == '__main__':
    main()