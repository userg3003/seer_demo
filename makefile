ifndef PIP
	PIP=pip
endif
ifndef PYTHON
	PYTHON=python
endif
PYTHONPATH=./
CMD_PATH=cmd/

STATIC_PATH=static/
UPLOAD_FOLDER=data/videos/
VIDEO_NAME=video.mp4

FACE_DETECTION_MODEL_PATH=data/trained_models/detection_models/haarcascade_frontalface_default.xml
EMOTION_MODEL_PATH=data/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5
CONFIG_EMOTION_MODEL_PATH=.config/emotion_model.json
LOG_LEVEL=INFO

SERVICE_NAME=seer
SERVICE_TEMPLATES_FOLDER=templates/


ENVS=IMAGE_REPORT_PATH=$(IMAGE_REPORT_PATH) UPLOAD_FOLDER=$(UPLOAD_FOLDER) VIDEO_NAME=${VIDEO_NAME} \
	FACE_DETECTION_MODEL_PATH=$(FACE_DETECTION_MODEL_PATH) EMOTION_MODEL_PATH=$(EMOTION_MODEL_PATH) \
	CONFIG_EMOTION_MODEL_PATH=$(CONFIG_EMOTION_MODEL_PATH) LOG_LEVEL=$(LOG_LEVEL) \
	SERVICE_NAME=$(SERVICE_NAME) SERVICE_TEMPLATES_FOLDER=$(SERVICE_TEMPLATES_FOLDER) \
	PYTHONPATH=$(PYTHONPATH) STATIC_PATH=$(STATIC_PATH)

run:
	$(info run starting...)
	$(info $(ENVS))
	$(ENVS) $(PYTHON) ${CMD_PATH}service.py

deps:
	$(info dependencies installing...)
	$(info $(ENVS))
	$(PIP) install -r requirements
