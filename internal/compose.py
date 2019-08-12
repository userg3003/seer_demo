import argparse
import json
import logging
from os import getenv


def desktop():
    args = argparse.ArgumentParser()
    args.add_argument(
        '--video-path',
        default=getenv('VIDEO_PATH', 0),
        help='path to video or camera',
    )
    args.add_argument(
        '--image-report-path',
        default=getenv('IMAGE_REPORT_PATH'),
        type=str,
        help='path to save image report',
    )
    args.add_argument(
        '--face-detection-model-path',
        default=getenv('FACE_DETECTION_MODEL_PATH'),
        type=str,
        help='path to face detection',
    )
    args.add_argument(
        '--emotion-model-path',
        default=getenv('EMOTION_MODEL_PATH'),
        type=str,
        help='path to emotion model path',
    )
    args.add_argument(
        '--config-emotion-model-path',
        default=getenv('CONFIG_EMOTION_MODEL_PATH'),
        type=str,
        help='path to models\'s config',
    )
    args.add_argument(
        '--log-level',
        default=getenv('LOG_LEVEL', 'INFO'),
        choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL'],
        type=lambda x: getattr(logging, x),
        help='level of logging',
    )
    args.add_argument(
        '--log-filename',
        default=getenv('LOG_FILENAME', None),
        type=str,
        help='path to file for logging or not set for logging to stdout',
    )
    kwargs = vars(args.parse_args())
    kwargs['emotion_model'] = json.load(open(kwargs['config_emotion_model_path']))
    return kwargs


def service():
    env1 = getenv('VIDEO_NAME')
    args = argparse.ArgumentParser()
    args.add_argument(
        '--video-name',
        default=getenv('VIDEO_NAME'),
        help='video file\'s name',
    )
    args.add_argument(
        '--upload-folder',
        default=getenv('UPLOAD_FOLDER'),
        help='path to video or camera',
    )
    args.add_argument(
        '--image-report-path',
        default=getenv('IMAGE_REPORT_PATH'),
        type=str,
        help='path to save image report',
    )
    args.add_argument(
        '--face-detection-model-path',
        default=getenv('FACE_DETECTION_MODEL_PATH'),
        type=str,
        help='path to face detection',
    )
    args.add_argument(
        '--emotion-model-path',
        default=getenv('EMOTION_MODEL_PATH'),
        type=str,
        help='path to emotion model path',
    )
    args.add_argument(
        '--service-name',
        default=getenv('SERVICE_NAME'),
        type=str,
        help='service name',
    )
    args.add_argument(
        '--config-emotion-model-path',
        default=getenv('CONFIG_EMOTION_MODEL_PATH'),
        type=str,
        help='path to models\'s config',
    )
    args.add_argument(
        '--log-level',
        default=getenv('LOG_LEVEL', 'INFO'),
        choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL'],
        type=lambda x: getattr(logging, x),
        help='level of logging',
    )
    args.add_argument(
        '--log-filename',
        default=getenv('LOG_FILENAME', None),
        type=str,
        help='path to file for logging or not set for logging to stdout',
    )
    kwargs = vars(args.parse_args())
    kwargs['emotion_model'] = json.load(open(kwargs['config_emotion_model_path']))

    kwargs['allowed_extension'] = set()
    kwargs['allowed_extension'].add('mp4')
    kwargs['allowed_extension'].add('avi')
    kwargs['static_path'] = getenv('STATIC_PATH')

    return kwargs
