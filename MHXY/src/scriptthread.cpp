#include "scriptthread.h"
#include "mainwindow.h"
#include <QFile>
#include <QTextStream>


ScriptThread::ScriptThread(MainWindow *mw)
{
    this->mw = mw;
    QScriptValue qcmu = engine.newQObject(this->mw);
    engine.globalObject().setProperty("XY", qcmu);
    QScriptValue st = engine.newQObject(this);
    engine.globalObject().setProperty("ST", st);
}

void ScriptThread::LoadScriptFile()
{
    //载入脚本
    //读取js文件
    QString fileName("script/main.js");
    QFile scriptFile(fileName);
    scriptFile.open(QIODevice::ReadOnly);
    QTextStream stream(&scriptFile);
    stream.setCodec("UTF-8");
    QString contents = stream.readAll();
    scriptFile.close();
    engine.evaluate(contents, "script/main.js");
    if(engine.hasUncaughtException()){

            QString errinfo =  engine.uncaughtException().toString();
            errinfo += engine.uncaughtExceptionBacktrace().join("/n");

            emit this->mw->SIGNAL_Add_Log_Msg(errinfo);
    }
}



void ScriptThread::run()
{

    engine.evaluate("main();");
    if(engine.hasUncaughtException()){

            QString errinfo =  engine.uncaughtException().toString();
            errinfo += engine.uncaughtExceptionBacktrace().join("/n");

           emit this->mw->SIGNAL_Add_Log_Msg(errinfo);
    }

}

//######################################## export

void ScriptThread::Sleep(int value)
{
    this->msleep(value);
}

void ScriptThread::Mouse_Move_To(int x, int y)
{
    hardKeyMouse.MouseMove(x,y);
}

void ScriptThread::Mouse_Click(int type, int sleep)
{
    hardKeyMouse.MouseClick(type,sleep);
}

void ScriptThread::Key_Click(int key1, int key2, int sleep)
{
   hardKeyMouse.KeyClick(key1,key2,sleep);
}
