#include "hardkeymouse.h"
#include <QDebug>
#include <QThread>

QLibrary *HardKeyMouse::dd = NULL;

HardKeyMouse::HardKeyMouse(QObject *parent) : QObject(parent)
{
    if(HardKeyMouse::dd == NULL){
        HardKeyMouse::dd = new QLibrary("./DD/DD32.dll");
        HardKeyMouse::dd->load();
        if(!HardKeyMouse::dd->isLoaded()){
            qDebug()<<"Load DD Fail!";
        }
    }
}

void HardKeyMouse::KeyClick(int key1,int key2)
{
    typedef void (*Fun)(int,int);
    Fun DD_key = (Fun)HardKeyMouse::dd->resolve("DD_key");
    DD_key(key1,1);
    if(key2>0){DD_key(key2,1);}
    QThread::msleep(50);
    DD_key(key1,2);
    if(key2>0){DD_key(key2,2);}
}

void HardKeyMouse::MouseClick(int button)
{
    typedef void (*Fun)(int);
    Fun DD_btn = (Fun)HardKeyMouse::dd->resolve("DD_btn");
    if(button==0){
        DD_btn(1);
        QThread::msleep(50);
        DD_btn(2);
    }else{
        DD_btn(4);
        QThread::msleep(50);
        DD_btn(8);
    }
}


void HardKeyMouse::MouseMove(int x,int y)
{
    typedef void (*Fun)(int,int);
    Fun DD_mov = (Fun)HardKeyMouse::dd->resolve("DD_mov");
    DD_mov(x,y);
}
