# Real-Time Object Detection with RTSP

Detect objects in real time using RTSP (Real-Time Streaming Protocol) and object detection model.

## Tech Stack

1. Backend is built on Python 3.11 [older versions are generally not recommended and py>3.12 don't have much updates in the supporting libraries]
2. OpenCV: Widely used computer vision library for video streaming and image processing. It is also fast and optimised for real-time applications.
   2.1 With OpenCV video capture object, either the video stream or video file can be read -> processed and released.
   2.2 For connecting actual real-time video, RTSP camera app can be used as RTSP server -> take its URL and input to the OpenCV cap object.
3. RTSP Stream: With IP Webcam
   Tested with Android’s IP Webcam app for stable RTSP streaming. iOS apps tested had unreliable H.264 encoding leading to decoding issues. IP Webcam allowed clean integration with OpenCV via RTSP.
