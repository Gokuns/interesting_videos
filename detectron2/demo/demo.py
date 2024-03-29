# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import glob
import multiprocessing as mp
import os
import time
import cv2
import tqdm
import json
from pathlib import Path

from config import argument_defaults
from detectron2.detectron2.config import get_cfg
from detectron2.detectron2.config import get_cfg
from detectron2.detectron2.data.detection_utils import read_image
from detectron2.detectron2.utils.logger import setup_logger
from detectron2 import opt_creator


from detectron2.demo.predictor import VisualizationDemo

# constants
WINDOW_NAME = "COCO detections"


def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 demo for builtin models")
    parser.add_argument(
        "--config-file",
        default="configs/quick_schedules/e2e_mask_rcnn_R_50_FPN_inference_acc_test.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--webcam", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--video-input", help="Path to video file.")
    parser.add_argument("--input", nargs="+", help="A list of space separated input images")
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser

def run(object, videos):
    WINDOW_NAME = "COCO detections"
    mp.set_start_method("spawn", force=True)
    #args = get_parser().parse_args()
    feats = opt_creator.FeatureBearer.getInstance()
    #TODO add a for loop for every scene and rerun main
    # with open("input") as f:
    #     videos = f.readlines()
    #video_name = "scene_1"
    curr_vid = 0
    frame_count = 0
    for video_name in videos:
        vid_path = Path(video_name)
        curr_vid += 1
        feats.features = []
        video_name= video_name.replace('\n', '')
        args = opt_creator.create_opt(video_name, argument_defaults['output_path'] + vid_path.name)
        logger = setup_logger()
        logger.info("Arguments: " + str(args))
        cfg = setup_cfg(args)

        demo = VisualizationDemo(cfg)

        if args.input:
            if len(args.input) == 1:
                args.input = glob.glob(os.path.expanduser(args.input[0]))
                assert args.input, "The input path(s) was not found"
            for path in tqdm.tqdm(args.input, disable=not args.output):
                # use PIL, to be consistent with evaluation
                img = read_image(path, format="BGR")
                start_time = time.time()
                predictions, visualized_output = demo.run_on_image(img)
                logger.info(
                    "{}: detected {} instances in {:.2f}s".format(
                        path, len(predictions["instances"]), time.time() - start_time
                    )
                )

                if args.output:
                    if os.path.isdir(args.output):
                        assert os.path.isdir(args.output), args.output
                        out_filename = os.path.join(args.output, os.path.basename(path))
                    else:
                        assert len(args.input) == 1, "Please specify a directory with args.output"
                        out_filename = args.output
                    visualized_output.save(out_filename)
                else:
                    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
                    cv2.imshow(WINDOW_NAME, visualized_output.get_image()[:, :, ::-1])
                    if cv2.waitKey(0) == 27:
                        break  # esc to quit

        elif args.webcam:
            assert args.input is None, "Cannot have both --input and --webcam!"
            cam = cv2.VideoCapture(0)
            for vis in tqdm.tqdm(demo.run_on_video(cam)):
                cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
                cv2.imshow(WINDOW_NAME, vis)
                if cv2.waitKey(1) == 27:
                    break  # esc to quit
            cv2.destroyAllWindows()
        elif args.video_input:
            video = cv2.VideoCapture(args.video_input)
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frames_per_second = video.get(cv2.CAP_PROP_FPS)
            num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            basename = os.path.basename(args.video_input)

            if args.output:
                if os.path.isdir(args.output):
                    output_fname = os.path.join(args.output, basename)
                    output_fname = os.path.splitext(output_fname)[0] + ".mp4"
                else:
                    output_fname = args.output
                if os.path.isfile(output_fname):
                    continue
                output_file = cv2.VideoWriter(
                    filename=output_fname,
                    # some installation of opencv may not support x264 (due to its license),
                    # you can try other format (e.g. MPEG)
                    fourcc=cv2.VideoWriter_fourcc(*"x264"),
                    fps=float(frames_per_second),
                    frameSize=(width, height),
                    isColor=True,
                )
            if not os.path.isfile(args.video_input):
                continue
            #assert os.path.isfile(args.video_input)

            curr_frame=0
            for vis_frame in tqdm.tqdm(demo.run_on_video(video), total=num_frames):
                curr_frame+=1
                frame_count+=1

                object.update_prog(video_name, curr_vid, curr_frame, num_frames, frame_count, len(videos))

                if args.output:
                    output_file.write(vis_frame)
                else:
                    #TODO commented out for it to run faster
                    cv2.namedWindow(basename, cv2.WINDOW_NORMAL)
                    cv2.imshow(basename, vis_frame)
                    if cv2.waitKey(1) == 27:
                        break  # esc to quit

            output = {vid_path.name: feats.features}

            video.release()
            with open(argument_defaults['extractor'] + vid_path.stem+ '.json', 'w') as outfile:
                json.dump(output, outfile)

            with open(argument_defaults['video_data_path'].format(argument_defaults['poc_mode']), 'r+') as dataset:
                data=json.load(dataset)
                print('read dataset')

            with open(argument_defaults['aggregation'] + 'max_pool' + '.json', 'r+') as agg:
                aggr=json.load(agg)
                print('read agg')

                # with open(
                #         argument_defaults['aggregation'] + 'average' + '.json', 'r+') as dataset:
                #     data = json.load(dataset)

            if args.output:
                output_file.release()
            else:
                cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
