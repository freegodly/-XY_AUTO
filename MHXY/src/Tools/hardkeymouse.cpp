#include "hardkeymouse.h"
#include <QDebug>
#include <QThread>


typedef void (*Fun)(int,int);
typedef void (*FunOne)(int);
HardKeyMouse::HardKeyMouse(QObject *parent) : QObject(parent)
{

    dd = new QLibrary("DD/DD32.dll");
    dd->load();
    if(!dd->isLoaded()){
        qDebug()<<"Load DD Fail!";
    }
//    dd=LoadLibrary(L"DD/DD32.dll");
//    if(dd==NULL)
//      {
//        FreeLibrary(dd);
//        qDebug()<<"Load DD Fail!";
//      }

}

void HardKeyMouse::KeyClick(int key1, int key2, int sleep)
{

    Fun DD_key = (Fun)dd->resolve("DD_key");
    //Fun DD_key = (Fun)GetProcAddress(dd,"DD_key");
    DD_key(key1,1);
    if(key2>0){DD_key(key2,1);}
    QThread::msleep(sleep);
    DD_key(key1,2);
    if(key2>0){DD_key(key2,2);}
}

void HardKeyMouse::MouseClick(int button, int sleep)
{

    FunOne DD_btn = (FunOne)dd->resolve("DD_btn");
    //FunOne DD_btn = (FunOne)GetProcAddress(dd,"DD_btn");
    if(button==0){
        DD_btn(1);
        QThread::msleep(sleep);
        DD_btn(2);
    }else{
        DD_btn(4);
        QThread::msleep(sleep);
        DD_btn(8);
    }
}


void HardKeyMouse::MouseMove(int x, int y)
{

    Fun DD_mov = (Fun)dd->resolve("DD_mov");
    //Fun DD_mov = (Fun)GetProcAddress(dd,"DD_mov");
    DD_mov(x,y);
}
