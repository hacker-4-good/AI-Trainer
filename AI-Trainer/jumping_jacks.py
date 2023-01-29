import mediapipe as mp
import cv2
from time import time
import math
import matplotlib.pyplot as plt



mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.9, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
f = 0
f1 = 1


def classifyPose_Easy(landmarks, output_image, count, display=False):
    global f, f1
    label = 'Unknown Pose'
    color = (0, 0, 255)

    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   

    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    angle1 = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])

    angle2 = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])

    if left_elbow_angle > 150 and left_elbow_angle < 195 and right_elbow_angle > 150 and right_elbow_angle < 195:
        if left_shoulder_angle > 70 and left_shoulder_angle < 100 and right_shoulder_angle > 70 and right_shoulder_angle < 100:
            if angle1 > 95 and angle2 > 95:
                label = 'Jumping Jacks'
                f = 1
                if(f and f1):
                    f1 = 0
                    count = count + 1
    else:
        f1 = 1

    if label != 'Unknown Pose':
        color = (0, 255, 0)  
        cv2.putText(output_image, f'{label}', (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
    
    cv2.putText(frame, "Easy Mode on", (350,100), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)
    cv2.putText(frame, 'Count: {}'.format(int(count)), (10, 200),cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    if display:
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off')
    else:
        return output_image, label, count










def classifyPose_Hard(landmarks, output_image, count, display=False):
    global f, f1
    label = 'Unknown Pose'
    color = (0, 0, 255)

    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   

    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    angle1 = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])

    angle2 = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
    
    leg_distance = DistanceCalculation(landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value])


    if left_elbow_angle > 160 and left_elbow_angle < 195 and right_elbow_angle > 160 and right_elbow_angle < 195:
        if left_shoulder_angle > 80 and left_shoulder_angle < 100 and right_shoulder_angle > 80 and right_shoulder_angle < 100:
            if angle1 > 100 and angle2 > 100:
                label = 'Jumping Jacks'
                f = 1
                if(f and f1):
                    f1 = 0
                    count = count + 1
    else:
        f1 = 1

    if label != 'Unknown Pose':
        color = (0, 255, 0)  
        cv2.putText(output_image, f'{label}', (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
        
    cv2.putText(frame, "Hard Mode on", (350,100), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)
    cv2.putText(frame, 'Count: {}'.format(int(count)), (10, 250),cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    if display:
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off')
    else:
        return output_image, label, count










def detectPose(image, pose, display=True):
    output_image = image.copy()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    height, width, _ = image.shape
    landmarks = []
    # if results.pose_landmarks:
    #     mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS)
    for landmark in results.pose_landmarks.landmark:
        landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))
            
    if display:
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1])
        plt.title("Original Image");plt.axis('off')
        plt.subplot(122);plt.imshow(output_image[:,:,::-1])
        plt.title("Output Image");plt.axis('off')
        mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS) 
    else:
        return output_image, landmarks









def DistanceCalculation(landmark1, landmark2):
    x1,y1,_ = landmark1
    x2,y2,_ = landmark2
    distance = math.sqrt((x1-x2)**2+(y1-y2)**2)
    return distance










def calculateAngle(landmark1, landmark2, landmark3):
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle <= 0:
        angle += 360
    return angle





mp_pose = mp.solutions.pose
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1) 
# video = cv2.VideoCapture("rtsp://admin:awicam6661@10.15.17.34:554/cam/realmonitor?channel=1&subtype=0")
# video = cv2.VideoCapture("C:\\Users\\mayan\\OneDrive\\Desktop\\VS Code\\Internship\\video.mp4")
video = cv2.VideoCapture("AI-Trainer/test.mp4")
# video = cv2.VideoCapture(0)

time1 = 0
time2 = 0
count = 0
check = 0
easy_check = 0
hard_check = 0

while video.isOpened():
    global ok, frame
    ok, frame = video.read()
    if not ok:
        break
    
    frame_height, frame_width, _ =  frame.shape
    frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640)) 
    frame, landmarks = detectPose(frame, pose_video, display=False)

    if(check==0):
        cv2.putText(frame, "Choose the difficulty", (320,150), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 5)
        cv2.putText(frame, "Hard", (200,300), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,255), 4)
        cv2.putText(frame, "Easy", (800,300), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,255), 4)
    try:
        a1, a2, _ = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        s1, s2,  _ = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        b1, c1, _ = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        p1, q1, _ = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        if(s1>a1 and s2<a2):
            easy_check = 1
        elif(b1<p1 and c1<q1):
            hard_check = 1
        
        if easy_check==1 and hard_check==0:
            check = 1
        if easy_check==0 and hard_check==1:
            check = 2
    except:
        pass

    if landmarks and check==1:
        frame, _ , count= classifyPose_Easy(landmarks, frame, count, display=False)
    elif landmarks and check==2:
        frame, _ , count= classifyPose_Hard(landmarks, frame, count, display=False)

    time2 = time()
    frames_per_second = 1.0 / (time2 - time1)
    cv2.putText(frame, 'FPS: {}'.format(int(frames_per_second)), (10, 100),cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
    cv2.putText(frame, 'check: {}'.format(int(check)), (10, 150),cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    time1 = time2
    cv2.imshow('Pose Detection', frame)
    k = cv2.waitKey(1)
    if(k == 27):
        break
    
video.release()
cv2.destroyAllWindows()