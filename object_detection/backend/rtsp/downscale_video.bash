ffmpeg -rtsp_transport tcp -i rtsp://192.168.2.78:8554/stream \
  -vf scale=640:480 -r 20 -b:v 1200k \
  -f rtsp rtsp://127.0.0.1:8555/downscaled