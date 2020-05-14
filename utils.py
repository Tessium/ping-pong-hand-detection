import numpy as np
import tensorflow as tf
import os
import cv2
import label_map_util

# set inference map locations
DIR = 'label_map'
PROTO_BUF = os.path.join(DIR, 'frozen_inference_graph.pb')
LABELS = os.path.join(DIR, 'hand_label_map.pbtxt')

# load inference graph and convert labels into categorical
label_map = label_map_util.load_labelmap(LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=1, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def load_inference_graph():
    """
    function to load frozen inference graph and create tensorflow session

    :return: tensorflow session with loaded graph
    """
    
    # create graph
    graph = tf.Graph()
    
    # read from path frozen inference graph
    # parse graph and load to memory
    with graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(PROTO_BUF, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        # create tensorflow session with loaded graph
        sess = tf.compat.v1.Session(graph=graph)

    return graph, sess


def draw(scores, boxes, w, h, frame):
    """
    function to draw box on the frame with given coordinates
 
    :param: scores: detected scores
    :param: boxes: detected boxes
    :param: w: width of frame
    :param: h: height of frame
    :param: frame: frame from video stream
    :return: center of y coordinates
    """
    # .2 is detection threshold
    if scores[0] > .2:
        # reformat coordinates from detected box
        x1, x2, y1, y2 = int(boxes[0][1] * w), int(boxes[0][3] * w), int(boxes[0][0] * h), int(boxes[0][2] * h)

        # draw rectangle on the given coordinates
        cv2.rectangle(frame, (x1, y1), (x2, y2), (77, 255, 9), 3, 1)

        # find center of y coordinates and return
        return (y1 + y2) / 2


def detect_objects(frame, detection_graph, sess):
    # load image, box, score, class tensors from graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')

    # add one more dimension to frame
    frame = np.expand_dims(frame, axis=0)

    # detected object from frame with loaded tensors
    boxes, scores = sess.run([detection_boxes, detection_scores], feed_dict={image_tensor: frame})

    # remove single dimensional elements from detected boxes and scores
    # return them
    return np.squeeze(boxes), np.squeeze(scores)
