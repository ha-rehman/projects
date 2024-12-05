import cv2

from Detector import YOLOV5_Detector

video_path = ""
vid = cv2.VideoCapture(video_path)
detector = YOLOV5_Detector(weights='yollov5s.pt',
                           img_size=640,
                           confidence_thres=0.5,
                           iou_thresh=0.45,
                           agnostic_nms=True,
                           augment=True)
while True:
    ret, frame = vid.read()
    if ret:
        res = detector.Detect(frame)
        cv2.imshow("Detection", res)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()
