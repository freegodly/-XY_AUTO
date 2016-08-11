#ifndef SCRIPTTHEARD_H
#define SCRIPTTHEARD_H

#include<QThread>
#include <QtScript>
#include <QObject>
#include "Tools/hardkeymouse.h"
class MainWindow;

class ScriptThread :public QThread
{
    Q_OBJECT
public:
    ScriptThread(MainWindow *mw);
    void LoadScriptFile();

public slots:
    void Sleep(int value);

    void Mouse_Move_To(int x , int y);

    void Mouse_Click(int type,int sleep);

    void Key_Click(int key1,int key2=-1,int sleep=100);

private:
     QScriptEngine engine;
     MainWindow *mw;
     HardKeyMouse hardKeyMouse;



     // QThread interface
protected:
     void run();
};

#endif // SCRIPTTHEARD_H
