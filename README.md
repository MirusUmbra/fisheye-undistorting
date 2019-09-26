fisheye undistorting
=

After knowing how to use api of opencv, including calibrating and undistorting, i wanted to figure out how  
the undistorting process work. So i viewed http://paulbourke.net/dome/fisheye/ and learnt projection from  
image to hemisphere surface, and wrote undistorting in my own way.

opencv version :
-
First my input datas of calibrateing chessboard will locate corner points, then give those points to fisheye  
calibrating of opencv which based on [Zhengyou Zhang's 1999 paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) , this will measure internal and external  
parameters, and distortion coefficients. So you can use those parameters 
to remap every pixels.</br>
I already have wrote functions including undistorting from image data, video data and stream.
	
no opencv version :
-
By following Paul's web, first you'd better consider every pixels with polar coordinates and sphere coordinates,  
using length and angle to describe pixels, then you can easily calculate whole projection. To undistort,  
all you need to do is to make every coordinates on hemisphere map to the new plane - your output plane.</br>
![projection](https://github.com/MirusUmbra/Display-data/raw/master/fisheye/projection.png)</br>
We can easily knowing what we actually want is phi and distance to the center of one point, using similar  
rectangle you can transform distance to center on output plane and input plane (this actually uses angle theta), 
and both output plane and input plane have same phi.</br>
I have wrote three version : without interpolation, with interpolation and optimizing with matrix. Dealing gray 
images only, and i didn't consider distorting parameters, maybe i will add it in future. I only upload last two 
version.</br>
Input:  
![mat](https://github.com/MirusUmbra/Display-data/raw/master/fisheye/201906281658402.png)</br>
Outputs in three way:  
![res1](https://github.com/MirusUmbra/Display-data/raw/master/fisheye/res.png)</br>
![res2](https://github.com/MirusUmbra/Display-data/raw/master/fisheye/r1.png)</br>
![res3](https://github.com/MirusUmbra/Display-data/raw/master/fisheye/r2.png)</br>

Per 640*480 image on my very old computer using second way cost 17.25s, and the last way cost 0.395s, speed  
up for 4300%


