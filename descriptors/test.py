import uvc
import cv2
dev_list = uvc.device_list()
print(dev_list)
cap = uvc.Capture(dev_list[0]["uid"])
print(cap.avaible_modes)
for x in range(10):
    print(x)
    cap.frame_mode = (640, 480, 30)
    for x in range(100):
        try:
            frame = cap.get_frame(1000)
        except uvc.StreamError as e:
            print(e)
        cv2.imshow("img",frame.gray)
        cv2.waitKey(1)