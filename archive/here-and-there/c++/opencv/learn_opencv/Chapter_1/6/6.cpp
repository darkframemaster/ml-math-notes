#include<opencv2/opencv.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>
using namespace cv;
using namespace std;
int main()
{
	//1.读入视频
	VideoCapture capture(0);

	//2.循环显示每一帧
	while(1)
	{
		Mat frame;
		capture>>frame;
		
		//模糊处理
		Mat dstImage;
		blur(frame,dstImage,Size(7,7));//Size(x,y) x为x方向的模糊度 y为y方向的模糊度
		//腐蚀处理
		Mat element=getStructuringElement(MORPH_RECT,Size(15,15));//Size(x,y) x,y为腐蚀的范围
		Mat dstImage2;
		erode(frame,dstImage2,element);
		//canny边缘检测
		Mat dstImage3,edge,grayImage;
		dstImage3.create(frame.size(),frame.type());
		cvtColor(frame,grayImage,CV_BGR2GRAY);
		blur(grayImage,edge,Size(3,3));
		Canny(edge,edge,3,9,3);
		
		imshow("正常视频",frame);
		imshow("模糊视频",dstImage);
		imshow("腐蚀视频",dstImage2);		
		imshow("边缘检测",edge);
		waitKey(0);
	}
	return 0;
}
