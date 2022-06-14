import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def mpPose(path):
    image1 = cv2.imread(path, 0)
    # cv2.imshow('graycsale image',image1)
    # cv2.waitKey(0)
    with mp_pose.Pose(
            static_image_mode=True, min_detection_confidence=0.5, model_complexity=2) as pose:
        results = pose.process(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
        try:
            landmarks = results.pose_landmarks.landmark
        except:
            pass
        # print(landmarks)
        # for connection in mp_pose.POSE_CONNECTIONS:
        #     print(connection)
        leftShoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]

        rightShoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        leftElbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]

        rightElbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]

        leftWrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]

        rightWrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

        leftHip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]

        rightHip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

        leftKnee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]

        rightKnee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]

        leftAnkle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]

        rightAnkle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        joints = [leftShoulder, rightShoulder, leftElbow, rightElbow, leftWrist, rightWrist,
                  leftHip, rightHip, leftKnee, rightKnee, leftAnkle, rightAnkle]

        #For connections, index 1,2,3,4,8,10 are most important
        connections = [(leftShoulder,rightShoulder),(leftShoulder,leftElbow),(leftElbow,leftWrist),
                       (rightShoulder,rightElbow),(rightElbow,rightWrist),
                       (leftShoulder,leftHip),(rightShoulder,rightHip),
                        (leftHip, rightHip), (leftHip, leftKnee), (leftKnee, leftAnkle),
                       (rightHip, rightKnee), (rightKnee, rightAnkle)]
        poseDictionary = {"Path": path, "Connections": connections, "Angles": []}
    print(path)

    return connections

def labelPicture(path):
    # Draw pose landmarks.
    image1 = cv2.imread(path, 0)
    # cv2.imshow('graycsale image',image1)
    # cv2.waitKey(0)
    with mp_pose.Pose(
            static_image_mode=True, min_detection_confidence=0.5, model_complexity=2) as pose:
        results = pose.process(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
        try:
            landmarks = results.pose_landmarks.landmark
        except:
            print("landmark error")
            pass
    BG_COLOR = (192, 192, 192)  # Grey
    annotated_image = image1.copy() #makes copy of image
    # condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    # bg_image = np.zeros(image1.shape, dtype=np.uint8)
    # bg_image[:] = BG_COLOR
    # annotated_image = np.where(condition, annotated_image, bg_image)
    mp_drawing.draw_landmarks( #draws on copy
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imwrite(f"processedPictures/{path}",annotated_image) #saves copy
    print(path)

