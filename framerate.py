# -*- coding: utf-8 -*-
# Framerate_Editor
# Copyright (C) 2022 Shane Atchley
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math
import argparse
import cv2

def progress_bar(progress, total, length = 30):
    complete_symbol = '█'
    incomplete_symbol = '-'
    bar_length = length
    if total == 0 or total is None:
        return
    completion = (progress / float(total))
    section_completion = int(completion * bar_length)
    percent_completion = 100 * completion
    complete = complete_symbol * section_completion
    incomplete = incomplete_symbol * (bar_length - section_completion)
    bar = complete + incomplete
    print(f"\r|{bar}| {percent_completion:.2f}%", end="\r")

def play(args):
    vid = cv2.VideoCapture((args.input_path))
    pos_frame = vid.get(1)
    while vid.isOpened():
        ret,frame = vid.read()
        if ret:
            cv2.imshow('frame', frame)
            pos_frame = vid.get(1)
            print(f"{pos_frame} frames")
        else:
            vid.set(1, pos_frame-1)
            print("Frame is not ready")
            cv2.waitKey(1000)
        if cv2.waitKey(10) == 27:
            break


    vid.release()
    cv2.destroyAllWindows()
    print("Finished")

def set_output_path(args):
    if args.output_path is not None:
        output = args.output_path
    else:
        output = args.input_path + "_output"
    return output

def run(args):
    output = set_output_path(args)
    
    print(f"Reading {args.input_path} \n")
    vid = cv2.VideoCapture(args.input_path)
    while not vid.isOpened():
        vid = cv2.VideoCapture(args.input_path)
        cv2.waitKey(1000)
        print("Wait for the header")
    original_width = int(vid.get(3))
    original_height = int(vid.get(4))
    print(f"Original video resolution is {original_width}x{original_height} \n")
    original_framerate = int(vid.get(5))
    print(f"Original video framerate is {original_framerate} \n")
    totalFrames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f"Original video has {totalFrames} total frames \n")
    frames = []
    timeout = []
    count = 0
    success = True
    speed = args.interval
    print(f"Saving every {speed} frames \n")
    outputfps = args.outputfps
    print(f"{outputfps} output FPS \n")

    writer = cv2.VideoWriter(output, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps=outputfps, frameSize=(original_width, original_height))

    print("Reading input file:")
    progress_bar(0, totalFrames)
    while True:
        if (len(timeout) == 5):
            vid.release()
            writer.release()
            break
        success, image = vid.read()
        if not success:
            timeout.append(1)
            continue
        else:
            timeout.clear()
            if (count % speed == 0):
                # frames.append(image)
                writer.write(image)
            count += 1
            # print(f"\r|{count}|", end="\r")
        progress_bar(count, totalFrames)
    
    
    # writer = cv2.VideoWriter(output, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps=outputfps, frameSize=(original_width, original_height))
    # print(f"Writing {len(frames)} frames output video to {output}: ")
    # progress_bar(0, len(frames))
    # for i, frame in enumerate(frames):
    #     writer.write(frame)
    #     progress_bar(i+1, len(frames))
    # writer.release()

def main():
    parser = argparse.ArgumentParser(description="Change the framerate of a video file")
    parser.add_argument("-speed", help="The number of frames to skip, use if shortening a video", dest="interval", type=int, required=False, default=1)
    parser.add_argument("-in", help="Input file path", dest="input_path", type=str, required=True)
    parser.add_argument("-out", help="Output file path, default is same as input", dest="output_path", type=str, required=False)
    parser.add_argument("-fps", help="Output fps", dest="outputfps", type=float, required=False, default=30)
    parser.add_argument("-", help="", dest="", type=int, required=False)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if (__name__ == "__main__"):
    main()


