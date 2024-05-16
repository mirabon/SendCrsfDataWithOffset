import cv2
import crsf_send

cap = cv2.VideoCapture('/dev/video1')
tracker = cv2.legacy.TrackerMOSSE.create()
ret, frame = cap.read()
bbox = cv2.selectROI("track", frame, False)
tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    success, bbox = tracker.update(frame)
    if success:
        # print(bbox)
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (255, 0, 0), 3)

        center_x = x + w / 2
        center_y = y + h / 2

        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2
        cv2.line(frame, (int(center_x), int(center_y)), (frame_center_x, frame_center_y), (0, 0, 255), 2)

        line_length = 20
        line_x1 = frame_center_x - line_length // 2
        line_x2 = frame_center_x + line_length // 2
        line_y1 = frame_center_y
        line_y2 = frame_center_y
        cv2.line(frame, (line_x1, line_y1), (line_x2, line_y2), (0, 0, 255), 2)

        line_x1 = frame_center_x
        line_x2 = frame_center_x
        line_y1 = frame_center_y - line_length // 2
        line_y2 = frame_center_y + line_length // 2
        cv2.line(frame, (line_x1, line_y1), (line_x2, line_y2), (0, 0, 255), 2)

        delta_x = frame_center_x - center_x
        delta_y = frame_center_y - center_y
        print((delta_x, delta_y))
        crsf_send.send_delta(delta_x, delta_y)
    else:
        print("object Lost")
    cv2.imshow("track", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
