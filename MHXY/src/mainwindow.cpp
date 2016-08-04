#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QScreen>
#include <QWindow>
#include <windows.h>

#include "Tools/tools.h"

#include <QImage>
#include <QDebug>
#include <ctime>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

   this->imgData = new uchar[640*480*3];

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::timerEvent(QTimerEvent *event)
{
    // 调用方法
    HWND hWnd = FindWindow(L"WSGAME",NULL);
    if(hWnd)
    {
        IplImage* Ipl_imagee  = Tools::GetDesktopHwndImage(hWnd);
        IplImage* Ipl_sub_image = Tools::GetSubImage(Ipl_imagee,cvRect(3,26,640,480));
        cvReleaseImage(&Ipl_imagee);


        find_obj(Ipl_sub_image);

        QImage* GameImage  = Tools::IplImageToQImage(Ipl_sub_image,this->imgData);
        cvReleaseImage(&Ipl_sub_image);

        QPixmap originalPixmap = QPixmap::fromImage(*GameImage);
        this->ui->GameRect->setPixmap(originalPixmap);
        ui_heroinfo_update();
    }
}

void MainWindow::on_pushButton_Test_clicked()
{

}

void MainWindow::on_actionStart_triggered()
{
    this->timer_id = this->startTimer(100);
}

void MainWindow::on_actionStop_triggered()
{
    this->killTimer(this->timer_id);
}

void MainWindow::find_obj(IplImage* Ipl_image)
{
    clock_t _start=clock();


    /////////////////////////
    /// 查找游戏鼠标位置
    ///
    /////////////////////////
    IplImage* p_image_mouse = cvLoadImage("feature/other/mouse.png",CV_LOAD_IMAGE_COLOR);
    IplImage* p_image_mouse_mask = cvLoadImage("feature/other/mouse_mask.png",CV_LOAD_IMAGE_GRAYSCALE);

    Find_Obj_Result result = Tools::find_obj_hist_mask(Ipl_image,p_image_mouse,p_image_mouse_mask,500);
    this->MousePoint.setX(result.x);
    this->MousePoint.setY(result.y);
    cvReleaseImage(&p_image_mouse);
    cvReleaseImage(&p_image_mouse_mask);

    /////////////////////////
    /// 查找游戏人物位置和地图名字
    ///
    /////////////////////////
    find_hero_location(Ipl_image);





    qDebug()<<"error:"<< result.error;


    qDebug()<<"Time:"<< float(clock() - _start) / CLK_TCK;
}

void MainWindow::find_hero_location(IplImage *Ipl_image)
{
    QSettings settings("feature/coordinates/coordinates.ini", QSettings::IniFormat);

    IplImage* sub_image = Tools::GetSubImage(Ipl_image,cvRect(20, 27,110,12));
    IplImage *  sub_image_gray = cvCreateImage(CvSize(sub_image->width,sub_image->height),sub_image->depth,1);

    cvCvtColor(sub_image,sub_image_gray,CV_BGR2GRAY); //关键

    cvThreshold(sub_image_gray, sub_image_gray, 200, 255, CV_THRESH_BINARY);

    //cvSaveImage("test.png",sub_image_gray);

    QList<Find_Obj_Result> find_list;
    //#先查找数字和汉字的分隔符
    IplImage* p_image_left = cvLoadImage("feature/coordinates/left.png",CV_LOAD_IMAGE_GRAYSCALE);
    cvThreshold(p_image_left, p_image_left, 200, 255, CV_THRESH_BINARY);
    find_list =  Tools::comparehits_bin_min(sub_image_gray,p_image_left,3);
    cvReleaseImage(&p_image_left);

    if(find_list.count() < 1) return;
    int left_x = find_list[0].x;
    qDebug()<<"left_x:"<< left_x;

    find_list.clear();
    IplImage* p_image_right = cvLoadImage("feature/coordinates/right.png",CV_LOAD_IMAGE_GRAYSCALE);
    cvThreshold(p_image_right, p_image_right, 200, 255, CV_THRESH_BINARY);
    find_list =  Tools::comparehits_bin_min(sub_image_gray,p_image_right,3);
    cvReleaseImage(&p_image_right);
    if(find_list.count() < 1) return;
    int right_x = find_list[0].x;
    qDebug()<<"right_x:"<< right_x;



    QList<Result_Feature_Info> RFI;


    //#匹配地图名字
    settings.beginGroup("names");
    QStringList names_keys = settings.childKeys();
    for(int i = 0 ; i< names_keys.count() ;i++){
        IplImage* p_image = cvLoadImage((QString("feature/coordinates/")+names_keys[i]).toStdString().c_str(),CV_LOAD_IMAGE_GRAYSCALE);
        cvThreshold(p_image, p_image, 200, 255, CV_THRESH_BINARY);
        find_list.clear();
        find_list =  Tools::comparehits_bin_min(sub_image_gray,p_image,2,0,left_x);
        cvReleaseImage(&p_image);
        foreach(Find_Obj_Result result, find_list){
            RFI.append({result,QString::fromUtf8(settings.value(names_keys[i]).toString().toStdString().c_str())});
        }
    }
    settings.endGroup();

    //#匹配坐标
    settings.beginGroup("numbers");
    QStringList numbers_keys = settings.childKeys();
    for(int i = 0 ; i< numbers_keys.count() ;i++){
        IplImage* p_image = cvLoadImage((QString("feature/coordinates/")+numbers_keys[i]).toStdString().c_str(),CV_LOAD_IMAGE_GRAYSCALE);
        cvThreshold(p_image, p_image, 200, 255, CV_THRESH_BINARY);
        find_list.clear();
        find_list =  Tools::comparehits_bin_min(sub_image_gray,p_image,2,left_x,0);
        cvReleaseImage(&p_image);
        foreach(Find_Obj_Result result, find_list){
            RFI.append({result,settings.value(numbers_keys[i]).toString()});
        }
    }
    settings.endGroup();

    //释放资源
    cvReleaseImage(&sub_image);
    cvReleaseImage(&sub_image_gray);


    //排序
    qSort(RFI.begin(),RFI.end(),
          [](Result_Feature_Info x,Result_Feature_Info y)->bool{
            return x.fresult.x < y.fresult.x;
    });

    QString str_location;
    foreach(Result_Feature_Info rf,RFI ){
        str_location+=rf.mean;
    }
    QStringList ls = str_location.split('[');
    this->MapName = ls[0];

    ls = ls[1].split(']')[0].split('@');

    this->HeroLocation.setX(ls[0].toInt());
    this->HeroLocation.setY(ls[1].toInt());
    qDebug()<<str_location;

}

void MainWindow::ui_heroinfo_update()
{
    QString str = QString("鼠标:[%1,%2]").arg(this->MousePoint.x()).arg(this->MousePoint.y());
    this->ui->l_MousePoint->setText(str);

    str = QString("人物坐标:[%1,%2]").arg(this->HeroLocation.x()).arg(this->HeroLocation.y());
    this->ui->l_HeroPoint->setText(str);

    str = QString("地图名称:%1").arg(this->MapName);
    this->ui->l_MapName->setText(str);
}
