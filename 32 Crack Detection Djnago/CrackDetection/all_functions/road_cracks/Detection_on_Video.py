import os

import cv2

from Detector import YOLOV5_Detector


def video_cracks(path):
    video_path = path
    vid = cv2.VideoCapture(video_path)
    print("++++++++++++++++++++++++++")
    detector = YOLOV5_Detector(weights=os.path.join(os.getcwd(), 'all_functions/road_cracks/My_model.pt'),
                               img_size=640,
                               confidence_thres=0.3,
                               iou_thresh=0.45,
                               agnostic_nms=True,
                               augment=True)
    frame_width = int(vid.get(3))
    frame_height = int(vid.get(4))

    size = (frame_width, frame_height)

    # Below VideoWriter object will create
    # a frame of above defined The output
    # is stored in 'filename.avi' file.
    # result = cv2.VideoWriter('video.avi',
    #                          cv2.VideoWriter_fourcc(*'MJPG'),
    #                          30, size)
    while vid.isOpened():
        ret, frame = vid.read()
        if ret:
            res, count_detection = detector.Detect(frame)
            cv2.imshow("Detection", res)
            # result.write(res)
            key = cv2.waitKey(1)
            print(frame.shape)
            if key == ord('q'):
                break

    vid.release()
    cv2.destroyAllWindows()
