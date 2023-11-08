FROM python:3.6.8
RUN cd / \
	&& git clone https://github.com/SmileCaoJ/plate_detection_recognition.git \
	&& cd plate_detection_recognition \
	&& pip install --upgrade pip \
	&& pip install -r requirements.txt --default-timeout=60000000 --no-cache-dir