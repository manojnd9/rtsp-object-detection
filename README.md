# Real-Time Object Detection with RTSP

A real-time object detection system that consumes RTSP video streams, detects objects using a YOLO-based model, stores results, and exposes APIs via FastAPI for interaction and monitoring.

## Tech Stack

- **Python 3.11**: Chosen due to compatibility with most up-to-date libraries and rich ecosystem for AI, helps for faster prototyping.
- **OpenCV**: Widely used computer vision library for real-time video streaming and image processing.
- **YOLOv8 (from Ultralytics)**: Pre-trained object detection model chosen for its balance of speed and accuracy. Supports CPU inference.
- **PostgreSQL + SQLAlchemy**: Relational database to store structured detection metadata. Managed via Alembic for migrations.
- **FastAPI**: For exposing APIs to control the streaming and object detection lifecycle.

## Tech Stack Choices

1. Backend is built on Python 3.11 [older versions are generally not recommended and py>3.12 don't have much updates in the supporting libraries]
2. OpenCV: Widely used computer vision library for video streaming and image processing. It is also fast and optimised for real-time applications.
   2.1 With OpenCV video capture object, either the video stream or video file can be read -> processed and released.
   2.2 For connecting actual real-time video, RTSP camera app can be used as RTSP server -> take its URL and input to the OpenCV cap object.
3. RTSP Stream: With IP Webcam
   Tested with Android’s IP Webcam app for stable RTSP streaming. iOS apps tested had unreliable H.264 encoding leading to decoding issues. IP Webcam allowed clean integration with OpenCV via RTSP.
4. Choosing object detection model
   - Due to real-time requirement, single stage detector is better. Amongst available models like YOLO (You Only Look Once), SSD (Single Stage Detector) and RetinaNet, YOLO is better as it is faster than others and has balance between speed and performance anc can be run on the CPU. And YOLO also has better community support. For skeleton implemenatation to get the framework running, YOLO is a best choice.
   - In YOLO, choosing the pre-trained model size impacts the speed and accuracy with nano being smallest/fastest upto extra-large which is most-accurate/slowest.

## Object Model Config and Stream URL setting

For the security purpose, `RTSP_STREAM_URL` is defined in `.env` file and loaded in the `main.py`.

Object model configuration can be added/modified in the `ModelSelector` dataclass and used in the `ObjectDetector` wrapper.

## Data Schema

1. `StreamSesssion` \
   Global session schema to help partion the way frames and detection results are stored.
2. `BoundingBox` and `DetectionResult` \
   Each detected object as a box has:
   - `timestamp`: at which the object was detected
   - `label`: name of of the object
   - `confidence`: confidence of detected objected by the model
   - `bbox`: bounding box coordinates
   - `frame_path`: path where input frame is stored
3. Storing streamed frames \
   - Save the running frame along with the timestamp within file name
     as jpg file. For now, the frames are stored in the local disk, for later it can be pushed to s3 buckets with proper partitioning.
   - Year, Month, Day and Session_ID is used to partion the folders to
     store the frames. It makes querying certain session data very fast.

## Database

PostgreSQL along with SQLAlchemy is used to manage the database storing and database sessions. This combination gives the advantage over schema control, querying and maintainace via alembic migrations.

The steaming session metadata and data of object detection results are stored in two different tables `streaming_sessions` and `detections` linked by `session_uuid`.
`streaming_sessions` stores the metadata like `year`, `month` and `day` along with unique `session_id`. This information is consumed by the partitioning and file name of streamed data.
With this the frames stored either locally or in cloud and the detection results can be traced easily with `streaming_session` data.

# Stream start-up options

When the rtsp streaming is started and the link to corresponding rtsp server is available, the video processing/object-detection functions can be triggered in two ways.

## CLI: Run main.py in the terminal

For local testing and development time, the `stream_url` can be set in the `.env` and main.py can be executed in the terminal.
This runs some boilerplate functions to `check the stream connection`, `selecting and instantiaing the object detection model` and `object containing the stream session metadata`.
These inputs are modular and are reused in another method of executing the real-time object detection.

## API Endpoints

This option enables the possibility to extend the object-detection implementation to be production ready!

FastAPI app is set-up in the `object_detection/backend/main_api.py`. This contains different routes to `start` the streaming session, `health` checkup and can be extended to many routes with desired functionalities.

To access and start the streaming and object detection in this way, the `FastAPI app` should be started with `uvicorn object_detection.backend.main_api:app --reload`.

This `app` also contains the `lifespan` function to execute `start-up` and `clean-up` functions when the app `starts` and `shuts down`.
