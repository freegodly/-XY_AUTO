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
#include <QTimer>


class ScriptThread;


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
    Q_PROPERTY( QList<int>      TempValueList           READ getTempValueList)

public:
    explicit MainWindow(QWidget *parent = 0);

    ~MainWindow();


protected:
    void timerEvent( QTimerEvent *event );

signals:
    void SIGNAL_Add_Log_Msg(QString msg);
    void SIGNAL_Clear_Log_Msg();
    void SIGNAL_Draw_Gamge_Rect(int x,int y,int w,int h);

public slots:
    void Add_Log_Msg(QString msg);

    void Clear_Log_Msg();

    QList<int> Match_Image_Rect(QString image_name,float mini_value = 0.8,int method=0);

    void Set_Gamge_ForegroundWindow();

    void Draw_Gamge_Rect(int x,int y,int w,int h);

private slots:

    void SLOT_Add_Log_Msg(QString msg);
    void SLOT_Clear_Log_Msg();
    void SLOT_Draw_Gamge_Rect(int x,int y,int w,int h);

    void on_pushButton_Test_clicked();

    void on_actionStart_triggered();

    void on_actionStop_triggered();

    void on_action_ScriptRun_triggered();

    void on_action_ScriptStop_triggered();

    void on_actionSelectWindow_triggered();

private:
    Ui::MainWindow *ui;
    int timer_id;
    ScriptThread *script;

    bool timer_status;
    HWND GameHwnd;

    cv::Mat p_Game_Image;
    QPixmap Game_originalPixmap;
    QList<QRect> PaintRectList;




public:

    QRect GameRect;

    QPoint MousePoint;
    QString MapName;
    QSize   MapSize;
    QSize  MiniMapSize;
    QPoint HeroLocation;
    QPoint MinimapmouseLocation;
    QList<int> TempValueList;

private:
    QList<int> getMousePoint();
    QString getMapName();
    QList<int>   getMapSize();
    QList<int>  getMiniMapSize();
    QList<int> getHeroLocation();
    QList<int> getMinimapmouseLocation();
    QList<int> getTempValueList();


private:
    void find_obj(cv::Mat& Ipl_image);
    void find_mouse_location(cv::Mat& Ipl_image);
    void find_hero_location(cv::Mat& Ipl_image);
    void find_minimapmouse_location(cv::Mat& Ipl_image);
    QPoint minimapmouse_location_sub(cv::Mat& Ipl_image,int type);
    void map_info_update();
    void ui_heroinfo_update();

    void run_script();
};

#endif // MAINWINDOW_H
