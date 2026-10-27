#include<opencv2/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>
#include<opencv2/opencv.hpp>
using namespace cv;
using namespace std;
int main()
{
	Mat srcImage=imread("1.jpg");
	imshow("腐蚀操作",srcImage);
//进行腐蚀操作
	Mat element=getStructuringElement(MORPH_RECT,Size(15,15));
	Mat dstImage;
	erode(srcImage,dstImage,element);
	
	imshow("效果图",dstImage);
	waitKey(0);
	return 0;
}
	
