/*
#include <opencv2/core/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "opencv2/opencv.hpp"
#include <iostream>
#include <string>
using namespace cv;
using namespace std;

int main( int,char **)
{
	VideoCapture video(0);
	if(!video.isOpened())
		return -1;
	Mat edges;
	namedWindow("edges",1);
	for(;;)
	{
		Mat frame;
		video >> frame;
		imshow("original",frame);
		cvtColor(frame,edges, COLOR_BGR2GRAY);
		GaussianBlur(edges, edges, Size(7,7), 1.5, 1.5);
        	Canny(edges, edges, 0, 30, 3);
        	imshow("edges", edges);
        	if(waitKey(30) >= 0) break;
	}
	return 0;
}
*/
#include <stdio.h>
#include <iostream>
#include <cstdio>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <ctime>
#include <sys/time.h>
using namespace cv;
using namespace std;
int img_width = 960;
int img_heigh = 720;
int main(int argc, const char * argv[]) {
	const clock_t begin_time = clock();
    VideoCapture cap(1);
    cap.set(3,img_width);
    cap.set(4,img_heigh);
    Mat frame;
    while (cap.read(frame)) {
    	timeval tp;
    	gettimeofday(&tp, NULL);
    	long int begin = tp.tv_sec * 1000 + tp.tv_usec / 1000;
    	flip(frame,frame,0);
    	Mat gray;
    	Mat right_img = frame(Rect(frame.cols/2, 0, frame.cols/2, frame.rows));
    	Mat left_img = frame(Rect(0,0,frame.cols/2, frame.rows));
    	cvtColor(frame, gray, CV_BGR2GRAY);
        imshow("Frame", frame);
        //imshow("left", left_img);
        //imshow("right", right_img);
        //imshow("Gray", gray);
        gettimeofday(&tp, NULL);
        long int end = tp.tv_sec * 1000 + tp.tv_usec / 1000; //get current timestamp in milliseconds
        cout << (end - begin)/1000 << endl;
        if (waitKey(1) == 'q') {
            break;
        }
    }
    return 0;
}
