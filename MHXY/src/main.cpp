#include "mainwindow.h"
#include <QApplication>

#include <opencv/cv.hpp>
#include <stdlib.h>
#include <windows.h>
#include <QGuiApplication>
#include <QScreen>
#include <QDebug>


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    a.addLibraryPath("dlls/");
    MainWindow w;
    w.show();


    return a.exec();
}
