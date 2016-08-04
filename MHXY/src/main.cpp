#include "mainwindow.h"
#include <QApplication>

#include <opencv/cv.hpp>
#include <stdlib.h>
#include <windows.h>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    IplImage* image = cvLoadImage( "filename.png", 1 );




    return a.exec();
}
