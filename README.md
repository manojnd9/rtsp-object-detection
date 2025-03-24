# Real-Time Object Detection with RTSP

## Project Description

A real-time object detection system that consumes RTSP video streams, detects objects using a YOLO-based model, stores results, and exposes APIs via FastAPI for interaction and monitoring.

## Tech Stack

- **Python 3.11**: Chosen due to compatibility with most up-to-date libraries and rich ecosystem for AI, helps for faster prototyping.
- **OpenCV**: Widely used computer vision library for real-time video streaming and image processing.
- **YOLOv8 (from Ultralytics)**: Pre-trained object detection model chosen for its balance of speed and accuracy. Supports CPU inference.
- **PostgreSQL + SQLAlchemy**: Relational database to store structured detection metadata. Managed via Alembic for migrations.
- **FastAPI**: For exposing APIs to control the streaming and object detection lifecycle.

## Installation and Setup

## 1. Pre-Requisites

```
pyenv
docker
poetry
```

## 2. Clone the Repository

```
git clone git@github.com:manojnd9/rtsp-object-detection.git
cd real-time-object-detection
```

## 3. Create and Configure .venv

Open in the editor of your choice (preferred VS Code)

Create .env file under `object_detection/backend/` and store the `DATABASE_URL`

For the production, environment variables can be set-up in the corresponding deployment platform.

```
e.g.
DATABASE_URL = "postgresql://user:password@localhost:5432/ObjectDetectionDb"
```

Install dependencies defined in the `pyproject.toml`.

```
poetry install
```

## 4. Setup Database

Executing following make command will:

- generate and start the postgres container and exposes it to the localhost port 5432, which is mentioned in the `DATABASE_URL` mentioned above.

```
make db_setup_and_initialise
```

The tables will be created upon starting the application.

# 5. Execution Options

When the rtsp streaming is started and the link to corresponding rtsp server is available, the video processing/object-detection functions can be triggered in two ways.

## 5.1 API Endpoints

This option enables the possibility to extend the object-detection implementation to be production ready!

Start the FastAPI app with following command. This runs uvicorn under the hood.

```
make dev
```

Open the `Swagger Documenation` in the browser at [http://127.0.0.1:8000/docs](!http://127.0.0.1:8000/docs) to access the following routes.

### Start Streaming

`POST /stream/start` takes following arguments and upon execution posts start real-time video stream processing in the backend.

```
{
  "stream_url": "rtsp://host:port/stream",
  "steam_name": "string",
  "device_name": "string", # Optional
  "device_id": "string", # Optional
  "sampling_rate": 30 # Default
}
```

Upon successful start of stream processing, this returns the `session_id` which is unique for the streaming session.

Note:

- This starts the process in the background in order to not block the api to access other endpoints. Therefore, to stop the background proces, the stream has to be killed.
- For the future, the video processing functions will be called with `threading` and `process_stop` endpoint will then be added to stop the threads without having to stop the streaming source!
- The real-time functionality + performance of the object detection/storage is always a trade-off. Depending on the server ability and model efficiency, either all streamed frames can be processed or
  every nth frame can be processed based on the defined `sampling_rate`.

`GET /health` to check the health of the api endpoint.

`GET /session_data/sessions` to get the latest 10 streaming session metadata.

These endpoints can be extended to `download` the `detection` results along with saved `frames` as `.zip` file for further use or training of another model.

## 5.2 CLI: Run main.py in the Terminal

To start processing the streaming session.

- Define the `RTSP_STREAM_URL` in `object_detection/backend/.env`

```
RTSP_STREAM_URL = "rtsp://192.168.2.87:8080/h264_ulaw.sdp"
```

- Execute main.py, which runs functions to `check the stream connection`, `selecting object detection model` and `processing and storing the raw and detection results`.

```
python object_detection/backend/main.py
```

Once the stream is being processed, the raw streamed frames are stored under `object_detection/backend/data` with the folder structure/partitioning which is planned to suit the production cloud storage e.g. `aws/s3` buckets for optimal extraction.

To stop the process, end the streaming source or kill the process in terminal.

## Architecture Diagram

![object_detection_architecture](docs/images/architecture_implemented.png)

Image above shows the architecture diagram for the current implementation of Real-Time Object Detection and Data Storage.

## Data Schema

![database_schema](docs/images/database_schema.png)

This represents the data model of the input streaming session and detection results. The detection results in this implementation shows some important parameters of detected results. However this is not limited to the defined model.
With the help of `alembic` migrations, this schema, both tables can be exapanded based on the requirement, without damanging current data present in the database.

Every `streamed frame` is stored with following folder structure and filenaming:

```
data/streamed_data/
├── YYYY/
│   └── MM/
│       └── DD/
│           └── session_id-<uuid>/
│               └── frame-<timestamp>.jpg

```

## System Design Rationale

### Object Detection Strategy

- YOLOv8 (single stage detector) is chosen for real-time detection with flexible model sizes (nano to xlarge).
- Supports CPU inference and has strong community support.
- In YOLO, choosing the pre-trained model size impacts the speed and accuracy with nano being smallest/fastest upto extra-large which is most-accurate/slowest. For the prototype and since running on laptop, nano model is chosen.

### RTSP Handling

- OpenCV, a widely used computer vision library for real-time video streaming and image processing. Its method -> cv2.VideoCapture connects directly to the RTSP stream.
- Frames are read, processed, and released in a loop. Additional sampling_rate (either in config.py when running locally or via API request parameter when running with FastAPI app) provided can help to make trade-off between speed and performance.
- Android IP Webcam tested for reliable H.264 stream. Also a higher resolution camera can be bottleneck when streams are processed one after other.

### Storage Strategy

- Raw frames stored locally with timestamp and session-based folders.
- Can be extended to S3 with structured partitions.
- Streaming metadata and object detection results stored in PostgreSQL via SQLAlchemy models.

### Modularity

- ModelSelector: easily swap detection model.
- ObjectDetector: core wrapper for processing logic.
- Can be extended to handle multiple streams concurrently using background tasks.

## Testing & CI/CD

- For all the classes/functions/methods, unit tests can be added with `pytest`.
- End-to-end integration test to test from streaming to processing/storing. This can be done with small video and expected results can be asserted to check the entire functionality.
- All these tests along with format check using `black` can be tested with `GitHub Actions` for every PR merge.
- Upon merge, docker images can be built and published to codeartifacts.

Future Enhancements

Concurrent stream handling with background task manager
Stream lifecycle management (pause/resume)
Push saved frames to S3
Model switching from API
Dashboard with WebSocket-based live view
GPU support for faster inference

## System Design for scalability

## License

This project is for the purpose of evaluation only.
