#ifndef TOOLS_H
#define TOOLS_H

#include <QObject>
#include <QScreen>
#include <QWindow>
#include <windows.h>
#include <opencv/cv.hpp>
#include <opencv2/opencv.hpp>
#include <QRect>

struct Find_Obj_Result{
     int x;
     int y;
     float error;
};


struct Result_Feature_Info{
    Find_Obj_Result fresult;
    QString mean;
};



class Tools : public QObject
{
    Q_OBJECT
public:
    explicit Tools(QObject *parent = 0);

public:
  static IplImage*  HBitmapToIpl     (HBITMAP            hBmp);
  static IplImage*  GetHwndImage     (HWND               hWnd);
  static QImage*    IplImageToQImage (IplImage *img,uchar *buff);
  static IplImage*  QImageToIplImage (QImage*      qImage);
  static IplImage*  GetDesktopHwndImage(HWND             hWnd);
  static IplImage*  GetSubImage      (IplImage *img , CvRect rect);


  static Find_Obj_Result find_obj_hist_mask(IplImage * trainImage,
                              IplImage * queryImage,
                              IplImage * mask=NULL,
                              float max_sum=100,
                              int bins = 30,
                              int startx = 0 ,int endx = 0,
                              int starty = 0 ,int endy = 0,
                              int move_px = 5,int move_py = 5);

  static CvRect  find_obj_matchtemplate(IplImage * trainImage,
                                        IplImage * queryImage,
                                        float min_value=0.9,
                                        int method = 0);

  static QList<Find_Obj_Result> comparehits_bin_min(IplImage * image_bin,
                                                           IplImage *featureimage_bin,
                                                           int max_sum =1,int startx =0,
                                                           int endx = 0,int move_px =1);
  static QList<Find_Obj_Result> comparehits_bin_min_x(IplImage * image_bin,
                                                             IplImage *featureimage_bin, IplImage *featureimage_bin_mask=NULL,
                                                             int max_sum = 255, int startx =0 ,
                                                             int endx=0,
                                                             int starty  = 0 , int endy=0,
                                                             int move_px = 1, int move_py = 1 );


signals:

public slots:
};

#endif // TOOLS_H
