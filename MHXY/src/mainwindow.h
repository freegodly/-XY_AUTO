#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPixmap>
#include <opencv/cv.hpp>
#include <QPoint>
#include <QSettings>
namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);

    ~MainWindow();


protected:
    void timerEvent( QTimerEvent *event );

private slots:
    void on_pushButton_Test_clicked();

    void on_actionStart_triggered();

    void on_actionStop_triggered();

private:
    Ui::MainWindow *ui;
    uchar *imgData;
    int timer_id;

    QPoint MousePoint;
    QString MapName;
    QPoint HeroLocation;

private:
    void find_obj(IplImage *Ipl_image);
    void find_hero_location(IplImage *Ipl_image);
    void ui_heroinfo_update();
};


#endif // MAINWINDOW_H
