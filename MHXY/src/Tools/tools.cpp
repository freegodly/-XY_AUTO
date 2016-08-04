#include "tools.h"
#include <QDebug>


Tools::Tools(QObject *parent) : QObject(parent)
{

}



// hbitmap convert to IplImage
IplImage* Tools::HBitmapToIpl(HBITMAP hBmp)
{
    BITMAP bmp;
    GetObject(hBmp,sizeof(BITMAP),&bmp);

    // get channels which equal 1 2 3 or 4
    // bmBitsPixel :
    // Specifies the number of bits
    // required to indicate the color of a pixel.
    int nChannels = bmp.bmBitsPixel == 1 ? 1 : bmp.bmBitsPixel/8 ;

    // get depth color bitmap or grayscale
    int depth = bmp.bmBitsPixel == 1 ? IPL_DEPTH_1U : IPL_DEPTH_8U;


    // create header image
    IplImage* img = cvCreateImage(cvSize(bmp.bmWidth,bmp.bmHeight),depth,nChannels);

    // allocat memory for the pBuffer
    BYTE *pBuffer = new BYTE[bmp.bmHeight*bmp.bmWidth*nChannels];

    // copies the bitmap bits of a specified device-dependent bitmap into a buffer
    GetBitmapBits(hBmp,bmp.bmHeight*bmp.bmWidth*nChannels,pBuffer);

    // copy data to the imagedata
    memcpy(img->imageData,pBuffer,bmp.bmHeight*bmp.bmWidth*nChannels);
    delete pBuffer;

    // create the image
    IplImage *dst = cvCreateImage(cvGetSize(img),img->depth,3);
    // convert color
    cvCvtColor(img,dst,CV_BGRA2BGR);
    cvReleaseImage(&img);
    return dst;
}


IplImage*  Tools::GetHwndImage(HWND hWnd)
{
    IplImage* image =NULL;

    HDC hDC = ::GetWindowDC(hWnd);

    HDC hMemDC = ::CreateCompatibleDC(hDC);

    RECT rc;
    ::GetWindowRect(hWnd, &rc);

    HBITMAP hBitmap = ::CreateCompatibleBitmap(hDC, rc.right - rc.left, rc.bottom - rc.top);


    HBITMAP hOldBmp = (HBITMAP)::SelectObject(hMemDC, hBitmap);
    ::PrintWindow(hWnd, hMemDC, 0);

    BITMAP bitmap = {0};
    ::GetObject(hBitmap, sizeof(BITMAP), &bitmap);
    BITMAPINFOHEADER bi = {0};
    BITMAPFILEHEADER bf = {0};

    CONST int nBitCount = 24;
    bi.biSize = sizeof(BITMAPINFOHEADER);
    bi.biWidth = bitmap.bmWidth;
    bi.biHeight = bitmap.bmHeight;
    bi.biPlanes = 1;
    bi.biBitCount = nBitCount;
    bi.biCompression = BI_RGB;
    DWORD dwSize = ((bitmap.bmWidth * nBitCount + 31) / 32) * 4 * bitmap.bmHeight;

    HANDLE hDib = GlobalAlloc(GHND, dwSize + sizeof(BITMAPINFOHEADER));
    LPBITMAPINFOHEADER lpbi = (LPBITMAPINFOHEADER)GlobalLock(hDib);
    *lpbi = bi;

    ::GetDIBits(hMemDC, hBitmap, 0, bitmap.bmHeight, (BYTE*)lpbi + sizeof(BITMAPINFOHEADER), (BITMAPINFO*)lpbi, DIB_RGB_COLORS);

    image = Tools::HBitmapToIpl(hBitmap);


    GlobalUnlock(hDib);
    GlobalFree(hDib);

    ::SelectObject(hMemDC, hOldBmp);
    ::DeleteObject(hBitmap);
    ::DeleteObject(hMemDC);
    ::ReleaseDC(hWnd, hDC);


    return image;
}



IplImage* Tools::GetDesktopHwndImage(HWND hWnd)
{
    IplImage* image =NULL;

    HWND hDesktop = ::GetDesktopWindow();
    if(NULL == hWnd)
    {
        hWnd = hDesktop;
    }
    RECT rect;
    ::GetWindowRect(hWnd, &rect);
    RECT client_rect;
    GetClientRect(hWnd,&client_rect);

    int nWidht = rect.right - rect.left;
    int nHeight = rect.bottom - rect.top;


    HDC hSrcDC = ::GetWindowDC(hWnd);
    HDC hMemDC = ::CreateCompatibleDC(hSrcDC);
    HBITMAP hBitmap = ::CreateCompatibleBitmap(hSrcDC, nWidht, nHeight);
    HBITMAP hOldBitmap = (HBITMAP)::SelectObject(hMemDC, hBitmap);
    ::BitBlt(hMemDC, 0, 0, nWidht, nHeight, hSrcDC, 0, 0, SRCCOPY);

    BITMAP bitmap = {0};
    ::GetObject(hBitmap, sizeof(BITMAP), &bitmap);
    BITMAPINFOHEADER bi = {0};
    BITMAPFILEHEADER bf = {0};

    CONST int nBitCount = 24;
    bi.biSize = sizeof(BITMAPINFOHEADER);
    bi.biWidth = bitmap.bmWidth;
    bi.biHeight = bitmap.bmHeight;
    bi.biPlanes = 1;
    bi.biBitCount = nBitCount;
    bi.biCompression = BI_RGB;
    DWORD dwSize = ((bitmap.bmWidth * nBitCount + 31) / 32) * 4 * bitmap.bmHeight;

    HANDLE hDib = GlobalAlloc(GHND, dwSize + sizeof(BITMAPINFOHEADER));
    LPBITMAPINFOHEADER lpbi = (LPBITMAPINFOHEADER)GlobalLock(hDib);
    *lpbi = bi;

    ::GetDIBits(hMemDC, hBitmap, 0, bitmap.bmHeight, (BYTE*)lpbi + sizeof(BITMAPINFOHEADER), (BITMAPINFO*)lpbi, DIB_RGB_COLORS);

    image = Tools::HBitmapToIpl(hBitmap);

    GlobalUnlock(hDib);
    GlobalFree(hDib);

    ::SelectObject(hMemDC, hOldBitmap);
    ::DeleteObject(hBitmap);
    ::DeleteDC(hMemDC);
    ::ReleaseDC(hWnd, hSrcDC);

    return image;
}


IplImage *Tools::GetSubImage( IplImage *img, CvRect rect)
{
     cvSetImageROI(img,rect);//设置源图像ROI
     IplImage* pDest = cvCreateImage(cvSize(rect.width,rect.height),img->depth,img->nChannels);//创建目标图像
     cvCopy(img,pDest); //复制图像
     cvResetImageROI(img);//源图像用完后，清空ROI
     return pDest;
}



QImage* Tools::IplImageToQImage(IplImage *img, uchar *buff)
{
    cvCvtColor((CvArr*)img,(CvArr*)img,CV_BGR2RGB);
    //uchar *imgData = new uchar[img->imageSize];
    memcpy(buff,img->imageData,img->imageSize);
    //uchar *imgData=(uchar *)img->imageData;
    QImage * image=new QImage(buff,img->width,img->height,QImage::Format_RGB888);

    return image;
}


IplImage *Tools::QImageToIplImage(QImage * qImage)
{
    int width = qImage->width();
    int height = qImage->height();
    CvSize Size;
    Size.height = height;
    Size.width = width;
    IplImage *IplImageBuffer = cvCreateImage(Size, IPL_DEPTH_8U, 3);
    for (int y = 0; y < height; ++y)
    {
        for (int x = 0; x < width; ++x)
        {
            QRgb rgb = qImage->pixel(x, y);
            cvSet2D(IplImageBuffer, y, x, CV_RGB(qRed(rgb), qGreen(rgb), qBlue(rgb)));
        }
    }
    return IplImageBuffer;
}








Find_Obj_Result Tools::find_obj_hist_mask(IplImage * trainImage,
                            IplImage * queryImage,
                            IplImage * mask,
                            float max_sum,
                            int bins ,
                            int startx  ,int endx ,
                            int starty  ,int endy,
                            int move_px ,int move_py)
{

    int    w = trainImage->width;
    int    h = trainImage->height;
    int    h_f = queryImage->height;
    int    w_f = queryImage->width;


    int    start_px = -1;
    int    start_py = -1;
    int    my_endx  = endx;
    int    my_endy  = endy;

    if (my_endx==0)
        my_endx = w;
    if (my_endy==0)
        my_endy = h;


    IplImage *  queryImage_b = cvCreateImage(CvSize(w_f,h_f),queryImage->depth,1);
    IplImage *  queryImage_g = cvCreateImage(CvSize(w_f,h_f),queryImage->depth,1);
    IplImage *  queryImage_r = cvCreateImage(CvSize(w_f,h_f),queryImage->depth,1);

    int bins_size[] = {bins};

    CvHistogram*    queryImage_b_hist = cvCreateHist(1,bins_size,CV_HIST_ARRAY);
    CvHistogram*    queryImage_g_hist = cvCreateHist(1,bins_size,CV_HIST_ARRAY);
    CvHistogram*    queryImage_r_hist = cvCreateHist(1,bins_size,CV_HIST_ARRAY);


    IplImage *  trainImage_b = cvCreateImage(CvSize(w_f,h_f),queryImage->depth,1);
    IplImage *  trainImage_g = cvCreateImage(CvSize(w_f,h_f),queryImage->depth,1);
    IplImage *  trainImage_r = cvCreateImage(CvSize(w_f,h_f),queryImage->depth,1);

    CvHistogram*    trainImage_b_hist = cvCreateHist(1,bins_size,CV_HIST_ARRAY);
    CvHistogram*    trainImage_g_hist = cvCreateHist(1,bins_size,CV_HIST_ARRAY);
    CvHistogram*    trainImage_r_hist = cvCreateHist(1,bins_size,CV_HIST_ARRAY);




    cvSplit(queryImage,queryImage_b,queryImage_g,queryImage_r,NULL);
    cvCalcHist(&queryImage_b,queryImage_b_hist,0,mask);
    cvCalcHist(&queryImage_g,queryImage_g_hist,0,mask);
    cvCalcHist(&queryImage_r,queryImage_r_hist,0,mask);

    double min_error  = max_sum;
    Find_Obj_Result result{-1,-1,-1.0};
    for(int  j =0; j< (int)((my_endy-starty-h_f)/move_py);j++ ){

        start_py = j*move_py+starty;
        for(int i=0;i< (int)((my_endx-startx-w_f)/move_px);i++ ){
            start_px = i*move_px+startx;
            cvSetImageROI(trainImage,cvRect((int)start_px,(int)start_py,w_f,h_f));
            cvSplit(trainImage,trainImage_b,trainImage_g,trainImage_r,NULL);
            cvCalcHist(&trainImage_b,trainImage_b_hist,0,mask);
            cvCalcHist(&trainImage_g,trainImage_g_hist,0,mask);
            cvCalcHist(&trainImage_r,trainImage_r_hist,0,mask);
            cvResetImageROI(trainImage);



            float now_error = 0.0;
            now_error = now_error + cvCompareHist(queryImage_b_hist,trainImage_b_hist,CV_COMP_CHISQR);
            now_error = now_error + cvCompareHist(queryImage_g_hist,trainImage_g_hist,CV_COMP_CHISQR);
            now_error = now_error + cvCompareHist(queryImage_r_hist,trainImage_r_hist,CV_COMP_CHISQR);

            if (now_error < min_error ){
                min_error = now_error;
                result =  {start_px,start_py,min_error};
               }
         }
    }

    cvReleaseHist(&queryImage_b_hist);
    cvReleaseHist(&queryImage_g_hist);
    cvReleaseHist(&queryImage_r_hist);
    cvReleaseHist(&trainImage_b_hist);
    cvReleaseHist(&trainImage_g_hist);
    cvReleaseHist(&trainImage_r_hist);

    cvReleaseImage(&queryImage_b);
    cvReleaseImage(&queryImage_g);
    cvReleaseImage(&queryImage_r);
    cvReleaseImage(&trainImage_b);
    cvReleaseImage(&trainImage_g);
    cvReleaseImage(&trainImage_r);


    return result;
  }


QList<Find_Obj_Result> Tools::comparehits_bin_min(IplImage * image_bin,
                    IplImage *featureimage_bin,
                    int max_sum,int startx  ,
                    int endx,int move_px )
{
      QList<Find_Obj_Result>   find_list;

      int h = image_bin->height;
      int w = image_bin->width;
      int h_f = featureimage_bin->height;
      int w_f = featureimage_bin->width;

      int bc_min = max_sum;
      int start_px = -1;

      if (endx==0) endx = w;
      for(int i=0;i< (int)(endx-startx-w_f)/move_px;i++)
      {
          start_px = i*move_px+startx;


          int error = 0;


          //rc = (start_px, 0, w_f, h_f)

          for(int j = 0 ; j<h_f;j++){
              for(int k = 0 ; k<w_f;k++){
                uchar f_value = ((uchar *)(featureimage_bin->imageData  +  j * featureimage_bin->widthStep ))[k];
                uchar im_value = ((uchar *)(image_bin->imageData  +  j * image_bin->widthStep ))[k+start_px];

                error += abs((int)f_value-(int)im_value);
              }
          }

          //qDebug()<<"error_______"<<error;
          if( error < bc_min){
              Find_Obj_Result result{start_px,0,error};
              find_list.append(result);
          }
      }
      qSort(find_list.begin(), find_list.end(),
                                [](Find_Obj_Result x,Find_Obj_Result y)->bool
                                                 {return x.error < y.error; });
      return find_list;

}


