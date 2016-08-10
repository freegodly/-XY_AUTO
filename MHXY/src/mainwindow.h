#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPixmap>
#include <opencv/cv.hpp>
#include <QPoint>
#include <QSettings>
#include "Tools/hardkeymouse.h"
#include <QSize>
#include <QtScript>
#include <QRect>
#include <QPainter>

namespace Ui {
class MainWindow;
}




class MainWindow : public QMainWindow
{
    Q_OBJECT
    Q_PROPERTY( QList<int>      MousePoint              READ getMousePoint)
    Q_PROPERTY( QString         MapName                 READ getMapName)
    Q_PROPERTY( QList<int>      MapSize                 READ getMapSize)
    Q_PROPERTY( QList<int>      MiniMapSize             READ getMiniMapSize)
    Q_PROPERTY( QList<int>      HeroLocation            READ getHeroLocation)
    Q_PROPERTY( QList<int>      MinimapmouseLocation    READ getMinimapmouseLocation)

public:
    explicit MainWindow(QWidget *parent = 0);

    ~MainWindow();


protected:
    void timerEvent( QTimerEvent *event );

public slots:
    void Add_Log_Msg(QString msg);

    void Clear_Log_Msg();

    void Mouse_Move_To(int x , int y);

    void Mouse_Click(int type);

    void Key_Click(int key1,int key2=-1);

    QList<int> Match_Image_Rect(QString image_name,float mini_value = 0.8,int method=0);

    void Set_Gamge_ForegroundWindow();

    void Draw_Gamge_Rect(int x,int y,int w,int h);

private slots:
    void on_pushButton_Test_clicked();

    void on_actionStart_triggered();

    void on_actionStop_triggered();

    void on_action_ScriptRun_triggered();

    void on_action_ScriptStop_triggered();

    void on_action_LoadScript_triggered();

    void on_actionSelectWindow_triggered();

private:
    Ui::MainWindow *ui;
    uchar *imgData;
    int timer_id;
    bool timer_status;
    HWND GameHwnd;
    QRect GameRect;
    QScriptEngine engine;

    HardKeyMouse hardKeyMouse;

    IplImage* p_Game_Image;

    QList<QRect> PaintRectList;


    bool IsRunScript;


public:
    QPoint MousePoint;
    QString MapName;
    QSize   MapSize;
    QSize  MiniMapSize;
    QPoint HeroLocation;
    QPoint MinimapmouseLocation;

private:
    QList<int> getMousePoint();
    QString getMapName();
    QList<int>   getMapSize();
    QList<int>  getMiniMapSize();
    QList<int> getHeroLocation();
    QList<int> getMinimapmouseLocation();


private:
    void find_obj(IplImage *Ipl_image);
    void find_mouse_location(IplImage *Ipl_image);
    void find_hero_location(IplImage *Ipl_image);
    void find_minimapmouse_location(IplImage *Ipl_image);
    QPoint minimapmouse_location_sub(IplImage *Ipl_image,int type);
    void map_info_update();
    void ui_heroinfo_update();
};

#endif // MAINWINDOW_H
