#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>
#include<opencv2/opencv.hpp>
using namespace cv;
using namespace std;
int main()
{	
	Mat srcImage=imread("1.jpg");
	imshow("滤波-原图",srcImage);
	Mat dstImage;
//进行均值滤波:
	blur(srcImage,dstImage,Size(7,7));
	imshow("滤波-效果图",dstImage);
	waitKey(0);
	return 0;
}
