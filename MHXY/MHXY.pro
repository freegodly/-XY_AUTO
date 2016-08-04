#-------------------------------------------------
#
# Project created by QtCreator 2016-08-04T10:19:22
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = MHXY
TEMPLATE = app

INCLUDEPATH += 3rd/opencv/include

LIBS += ../MHXY/3rd/opencv/lib/*.a


SOURCES += src/main.cpp\
       src/mainwindow.cpp

HEADERS  += src/mainwindow.h

FORMS    += src/mainwindow.ui

