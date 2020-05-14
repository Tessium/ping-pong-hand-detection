import utils 
import cv2

# load inference graph and tensorflow session
graph, sess = utils.load_inference_graph()


def init_cap(width, height):
    """
    function to initialize video capture object
    0 for webcam
    
    :param: width: width of frame 
    :param: height: height of frame 
    
    :return: videocapture object 

    """

    # create videocapture object
    # set width and height
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    return cap


def get_pos(cap):
    """
    function to get coordinates of hand in the frame

    :param: cap: videocapture object

    :return: median of y coordinate of detected hand

    """

    # get width and heigth of frame
    width, height = (cap.get(3), cap.get(4))

    # read frame
    ret, frame = cap.read()

    # convert frame from BGR to RGM
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # get coordinate and score of detected hand
    boxes, scores = utils.detect_objects(frame, graph, sess)

    # draw box on the detected coordinates in the frame 
    center = utils.draw(scores, boxes, width, height, frame)

    # show processed frame in the window
    cv2.imshow('Detection', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    # wait for 'q' key press
    # if pressed, window is closed and negative number returned
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        return -1
    
    # if hand detected, return center of y coordinates
    if center:
        return center
