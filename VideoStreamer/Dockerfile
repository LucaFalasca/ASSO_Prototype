FROM debian:bookworm-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
RUN apt-get install -y gcc
RUN apt-get install -y yt-dlp

COPY . .

# RUN gst-launch-1.0 filesrc location=50_ways_to_fall.mp4 ! \
#     decodebin ! \
#     videoconvert ! \
#     x264enc tune=zerolatency bitrate=2000 ! \
#     rtph264pay ! \
#     udpsink host=127.0.0.1 port=5000 sync=true

CMD ["gst-launch-1.0", "filesrc", "location=50_ways_to_fall.mp4", "!", "decodebin", "!", "videoconvert", "!", "x264enc", "tune=zerolatency", "bitrate=2000", "!", "mpegtsmux", "!", "udpsink", "host=vision_detector", "port=5000", "sync=true"]