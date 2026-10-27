#include<opencv2/opencv.hpp>
#include<opencv2/imgproc/imgproc.hpp>
using namespace std;
using namespace cv;
int main(){
	Mat srcImage=imread("1.jpg");
	
	imshow("canny边缘检测",srcImage);
	Mat dstImage,edge,grayImage;	//参数定义
	
	//1.创建与src同类型和大小的矩阵（dst）
	dstImage.create(srcImage.size(),srcImage.type());
		
	//2.将原图转换为灰度图像
	//opencv2
	cvtColor(srcImage,grayImage,CV_BGR2GRAY);
	//opencv3
	//cvtColor(srcImage,grayImage,COLOR_BGR3GRAY);

	//3.使用3*3内核来降噪
	blur(grayImage,edge,Size(3,3));
	
	//4.运行Canny算子
	Canny(edge,edge,3,9,3);
	
	//5.显示效果图
	imshow("效果图",edge);
	
	waitKey(0);
	return 0;
}	
