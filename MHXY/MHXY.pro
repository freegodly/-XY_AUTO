#-------------------------------------------------
#
# Project created by QtCreator 2016-08-04T10:19:22
#
#-------------------------------------------------

QT       += core gui script

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = MHXY
TEMPLATE = app

INCLUDEPATH += 3rd/opencv/include

LIBS += ../MHXY/3rd/opencv/lib/*.a -lgdi32

QMAKE_LFLAGS += -O0

SOURCES += src/main.cpp\
       src/mainwindow.cpp \
    src/Tools/tools.cpp \
    src/Tools/hardkeymouse.cpp \
    src/ui/selectwindowdialog.cpp

HEADERS  += src/mainwindow.h \
    src/Tools/tools.h \
    src/Tools/hardkeymouse.h \
    src/ui/selectwindowdialog.h

FORMS    += src/mainwindow.ui \
    src/ui/selectwindowdialog.ui

