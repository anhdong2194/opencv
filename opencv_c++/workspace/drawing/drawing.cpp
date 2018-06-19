#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/objdetect.hpp>

using namespace cv;

int main()
{
	Mat image = Mat::zeros (400,400,CV_8UC3);
	line(image,Point(15,20),Point(70,50),Scalar(110,220,0),2,8);
	circle(image,Point(200,200),32.0,Scalar(0,0,255),1,8);
	imshow("image",image);
	
	waitKey(0);
	return(0);
}
