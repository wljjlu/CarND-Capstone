from styx_msgs.msg import TrafficLight
import tensorflow as tf
import numpy as np
#from PIL import Image
#from PIL import ImageDraw
#from PIL import ImageColor

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        cmap = ImageColor.colormap
	COLOR_LIST = sorted([c for c in cmap.key()])



	SSD_GRAPH_FILE = 'ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb'
	self.detection_graph = load_graph(SSD_GRAPH_FILE)
	# The input placeholder for the image.
	# `get_tensor_by_name` returns the Tensor with the associated name in the Graph.
	self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

	# Each box represents a part of the image where a particular object was detected.
	self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

	# Each score represent how level of confidence for each of the objects.
	# Score is shown on the result image, together with the class label.
	self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')

	# The classification of the object (integer id).
	self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	self.sess = tf.Session(graph=detection_graph, config=config) 

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
	#image = Image.open('./assets/samples/27166.png')
	image = cv2.cvtColor(image, cv2.Color_BGR2RGB)
	image_np = np.expand_dims(np.asarray(image, dtype=np.uint8), 0)

	               
    	# Actual detection.
    	(boxes, scores, classes) = self.sess.run([self.detection_boxes, self.detection_scores, self.detection_classes], feed_dict={self.image_tensor: image_np})

    	# Remove unnecessary dimensions
    	boxes = np.squeeze(boxes)
    	scores = np.squeeze(scores)
    	classes = np.squeeze(classes)

    	confidence_cutoff = 0.3
    	# Filter boxes with a confidence score less than `confidence_cutoff`
    	boxes, scores, classes = filter_boxes(confidence_cutoff, boxes, scores, classes)

    	# The current box coordinates are normalized to a range between 0 and 1.
    	# This converts the coordinates actual location on the image.
    	#width, height = image.size
    	#box_coords = to_image_coords(boxes, height, width)

        return TrafficLight.UNKNOWN

def filter_boxes(min_score, boxes, scores, classes):
    """Return boxes with a confidence >= `min_score`"""
    n = len(classes)
    idxs = []
    for i in range(n):
        if scores[i] >= min_score and classes[i]==10 :
	    rospy.logwarn('traffic liaght detected', 
               min_j1, max_j1, clamped_j1)
            idxs.append(i)
    
    filtered_boxes = boxes[idxs, ...]
    filtered_scores = scores[idxs, ...]
    filtered_classes = classes[idxs, ...]
    return filtered_boxes, filtered_scores, filtered_classes

def to_image_coords(boxes, height, width):
    """
    The original box coordinate output is normalized, i.e [0, 1].
    
    This converts it back to the original coordinate based on the image
    size.
    """
    box_coords = np.zeros_like(boxes)
    box_coords[:, 0] = boxes[:, 0] * height
    box_coords[:, 1] = boxes[:, 1] * width
    box_coords[:, 2] = boxes[:, 2] * height
    box_coords[:, 3] = boxes[:, 3] * width
    
    return box_coords

def load_graph(graph_file):
    """Loads a frozen inference graph"""
    graph = tf.Graph()
    with graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(graph_file, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    return graph