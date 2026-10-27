#include<opencv2/opencv.hpp>
using namespace std;
using namespace cv;
int main()
{
	Mat srcImage=imread("1.jpg");
	imshow("hello，长颈鹿",srcImage);
	waitKey(0);
	return 0;
}
