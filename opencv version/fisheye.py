import cv2
import numpy as np

# storage chessboard coordinates
objpt = np.zeros((1, border_size[0] * border_size[1], 3), np.float32)
objpt[0, :, :2] = np.mgrid[0:border_size[0], 0:border_size[1]].T.reshape(-1, 2)


# dealing data
def findchesscorner(img_fld, img_path_list):
    img_shape_ = None
    objpoints = []
    imgpoints = []
    gary_shape = ()
    for i in img_path_list:
        src_img = cv2.imread(i, -1)
        src_img_g = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
        gary_shape = src_img_g.shape[::-1]
        if img_shape_:
            assert img_shape_ == gary_shape, "All images must share the same size."
        else:
            img_shape_ = gary_shape
        found, corners = cv2.findChessboardCorners(src_img_g, border_size, flags=cv2.CALIB_CB_ADAPTIVE_THRESH)
        if found:
            # subpix corret coordinate
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            cv2.cornerSubPix(src_img_g, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)
            objpoints.append(objpt)

    return objpoints, imgpoints, gary_shape
    
    
# measure camera parameters using data
def calib(objpoints, imgpoints, img_shape):
    # internal
    K = np.zeros((3, 3))
    # distort
    D = np.zeros((4, 1))
    # extranal
    R = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(len(objpoints))]
    T = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(len(objpoints))]

    rms, _, _, _, _ = cv2.fisheye.calibrate(
        objpoints,
        imgpoints,
        img_shape,
        K,
        D,
        R,
        T,
        cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_FIX_SKEW,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
    )

    new_K = None
    ## you can set area size use below function
    # balance = 1.5
    # new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, img_shape, np.eye(3), balance=balance)

    return K, D, new_K
    
 
 # undistorting by using camera parameters
 # undistorting images
 # here DIM are gary_shape from findchesscorner return
 def undistort(undistort_img_path_list, DIM, K, D, new_K=None):
    if new_K is None:
        new_K = K

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, DIM, cv2.CV_16SC2)
    for i in undistort_img_path_list:
        per_img = cv2.imread(i, -1)
        undistorted_img = cv2.remap(per_img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        # jobs done
        
        
# undistorting videos
def test_fix_video(DIM, K, D, new_K=None):
    if new_K is None:
        new_K = K
    cap = cv2.VideoCapture(undistort_video)

    fcc = cv2.VideoWriter_fourcc(*'XVID')
    # output video file
    out = cv2.VideoWriter('out.mp4', fcc, 20.0, (640, 480))

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, DIM, cv2.CV_16SC2)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            undistorted_img = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR,
                                        borderMode=cv2.BORDER_CONSTANT)
            out.write(undistorted_img)
        else:
            break

    cap.release()
    out.release()
    
    
# undistorting rtsp stream
def test_handle_rtsp(DIM, K, D, new_K, url=''):
    if not len(url):
        return

    if new_K is None:
        new_K = K

    cap = cv2.VideoCapture(url)

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, DIM, cv2.CV_16SC2)
    while 1:
        ret, frame = cap.read()
        if ret:
            undistorted_img = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR,
                                        borderMode=cv2.BORDER_CONSTANT)
			# display stream
            cv2.imshow("stream", undistorted_img)
            cv2.waitKey(1)
        else:
            break

    cap.release()
