#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QScreen>
#include <QWindow>
#include <windows.h>

#include "Tools/tools.h"

#include <QImage>
#include <QDebug>
#include <ctime>
#include <QPainter>
#include <QScriptValue>
#include "ui/selectwindowdialog.h"
#include <QDesktopWidget>
#include <QScreen>
#include "scriptthread.h"





MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    connect(this,SIGNAL(SIGNAL_Add_Log_Msg(QString)),this,SLOT(SLOT_Add_Log_Msg(QString)));
    connect(this,SIGNAL(SIGNAL_Clear_Log_Msg()),this,SLOT(SLOT_Clear_Log_Msg()));

    connect(this,SIGNAL(SIGNAL_Draw_Gamge_Rect(int,int,int,int)),this,SLOT(SLOT_Draw_Gamge_Rect(int,int,int,int)));

   timer_status = false;



   GameHwnd = FindWindow(L"WSGAME",NULL);


   script  = NULL;
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::timerEvent(QTimerEvent *event)
{

    // 调用方法
    if(GameHwnd)
    {
        RECT rect;
        GetWindowRect(GameHwnd, &rect);
        if(rect.left < 0) return;

        GameRect = {rect.left+3,rect.top+26,640,480};

        QScreen *screen = QGuiApplication::primaryScreen();

        Game_originalPixmap=screen->grabWindow(QApplication::desktop()->winId(),rect.left+3,rect.top+26,640,480);

        QImage image = Game_originalPixmap.toImage();
        cv::Mat mat = Tools::QImageTocvMat(image);



        p_Game_Image = mat;


        find_obj(p_Game_Image);


        map_info_update();
        ui_heroinfo_update();


        QPainter painter(&Game_originalPixmap);


        //////
        /// \brief 绘制标记
        ///

        painter.setPen(Qt::red);
        painter.drawRect(20, 27,110,12);

        painter.drawRect(MousePoint.x(), MousePoint.y(),26,25);

        int startx = this->MousePoint.x()-34;
        int starty = this->MousePoint.y()-26-5;
        painter.setBrush(QBrush(Qt::red, Qt::NoBrush));
        painter.drawRect(startx, starty,68,26);

        startx = this->MousePoint.x()-34;
        starty = this->MousePoint.y()+27;
        painter.drawRect(startx, starty,68,26);

        painter.setPen(Qt::red);
        foreach(QRect rc,PaintRectList){
            painter.drawRect(rc.x(),rc.y(),rc.width(),rc.height());
        }
        PaintRectList.clear();

        painter.end();
        this->ui->GameRect->setPixmap(Game_originalPixmap);

    }
}



//########################################导出方法

void MainWindow::Add_Log_Msg(QString msg)
{
    emit SIGNAL_Add_Log_Msg(msg);
}

void MainWindow::Clear_Log_Msg()
{
    emit SIGNAL_Clear_Log_Msg();
}

QList<int> MainWindow::Match_Image_Rect(QString image_name, float mini_value, int method)
{
    QList<int> qrect={-1,-1,0,0};

    cv::Mat  p_image_mouse = cv::imread(image_name.toStdString().c_str(),cv::IMREAD_COLOR);
    cv::Mat Game_Image = this->p_Game_Image.clone();
    CvRect rect=  Tools::cv_find_obj_matchtemplate(Game_Image,p_image_mouse,mini_value,method);

    qrect = {rect.x,rect.y,rect.width,rect.height};
    return qrect;
}

void MainWindow::Set_Gamge_ForegroundWindow()
{
    if(GameHwnd){
       SetForegroundWindow(GameHwnd);
    }
}

void MainWindow::Draw_Gamge_Rect(int x, int y, int w, int h)
{
    emit SIGNAL_Draw_Gamge_Rect(x,y,w,h);
}


//#######################################信号曹

void MainWindow::SLOT_Add_Log_Msg(QString msg)
{
     ui->t_RunLog->append(msg);
}

void MainWindow::SLOT_Clear_Log_Msg()
{
     ui->t_RunLog->clear();
}



void MainWindow::SLOT_Draw_Gamge_Rect(int x, int y, int w, int h)
{
     PaintRectList.append({x,y,w,h});
}



//########################################  事件


void MainWindow::on_pushButton_Test_clicked()
{

}

void MainWindow::on_actionStart_triggered()
{
    if(!timer_status){
        this->timer_id = this->startTimer(200);
        timer_status = true;
    }
}

void MainWindow::on_actionStop_triggered()
{
    this->killTimer(this->timer_id);
    timer_status = false;
}

void MainWindow::on_action_ScriptRun_triggered()
{
    if(script==NULL)
    {
       script = new ScriptThread(this);
       script->LoadScriptFile();
       script->start();
    }

}


void MainWindow::on_action_ScriptStop_triggered()
{
    if(script != NULL){

         script->terminate();
         //script->exit();
         script = NULL;
    }

}

void MainWindow::on_actionSelectWindow_triggered()
{


    SelectWindowDialog swd;
    swd.exec();
    GameHwnd = swd.Select_Hwnd;
    qDebug()<<GameHwnd;
}


//########################################  主要方法

void MainWindow::find_obj(cv::Mat &Ipl_image)
{
    clock_t _start=clock();


    /////////////////////////
    /// 查找游戏鼠标位置
    ///
    /////////////////////////
    find_mouse_location(Ipl_image);


    /////////////////////////
    /// 查找游戏人物位置和地图名字
    ///
    /////////////////////////
    find_hero_location(Ipl_image);

    /////////////////////////
    /// 查找游戏小地图鼠标指向的坐标
    ///
    /////////////////////////
    find_minimapmouse_location(Ipl_image);

    //qDebug()<<"error:"<< result.error;


    //qDebug()<<"Time:"<< float(clock() - _start) / CLK_TCK;
}

void MainWindow::find_mouse_location(cv::Mat &Ipl_image)
{
    // function 1

//    IplImage* p_image_mouse = cvLoadImage("feature/other/mouse.png",CV_LOAD_IMAGE_COLOR);
//    IplImage* p_image_mouse_mask = cvLoadImage("feature/other/mouse_mask.png",CV_LOAD_IMAGE_GRAYSCALE);

//    Find_Obj_Result result = Tools::find_obj_hist_mask(Ipl_image,p_image_mouse,p_image_mouse_mask,500);
//    this->MousePoint.setX(result.x);
//    this->MousePoint.setY(result.y);
//    cvReleaseImage(&p_image_mouse);
//    cvReleaseImage(&p_image_mouse_mask);


    // function 2
    //IplImage* p_image_mouse = cvLoadImage("feature/other/mouse_s.png",CV_LOAD_IMAGE_COLOR);

    cv::Mat p_image_mouse = cv::imread("feature/other/mouse_s.png",cv::IMREAD_COLOR);

    CvRect rect=  Tools::cv_find_obj_matchtemplate(Ipl_image,p_image_mouse,0.97,0);


    this->MousePoint.setX(rect.x-10);
    this->MousePoint.setY(rect.y-10);

}

void MainWindow::find_hero_location(cv::Mat &Ipl_image)
{
    QSettings settings("feature/coordinates/coordinates.ini", QSettings::IniFormat);
    settings.setIniCodec("UTF8");

    cv::Mat sub_image = Tools::cvGetSubImage(Ipl_image,cv::Rect(20, 27,110,12));
    cv::Mat sub_image_gray =cv::Mat(sub_image.rows,sub_image.cols,CV_8UC1);

    cv::cvtColor(sub_image,sub_image_gray,CV_BGR2GRAY);

    cv::threshold(sub_image_gray,sub_image_gray,200,255,CV_THRESH_BINARY);

    //cvSaveImage("test.png",sub_image_gray);

    QList<Find_Obj_Result> find_list;
    //#先查找数字和汉字的分隔符
    //IplImage* p_image_left = cvLoadImage("feature/coordinates/left.png",CV_LOAD_IMAGE_GRAYSCALE);
    cv::Mat p_image_left = cv::imread("feature/coordinates/left.png",cv::IMREAD_GRAYSCALE);
    cv::threshold(p_image_left,p_image_left,200,255,CV_THRESH_BINARY);
    //cvThreshold(p_image_left, p_image_left, 200, 255, CV_THRESH_BINARY);
    find_list =  Tools::cv_comparehits_bin_min(sub_image_gray,p_image_left,3);

    if(find_list.count() < 1) return;
    int left_x = find_list[0].x;
    //qDebug()<<"left_x:"<< left_x;

    find_list.clear();
    //IplImage* p_image_right = cvLoadImage("feature/coordinates/right.png",CV_LOAD_IMAGE_GRAYSCALE);
    //cvThreshold(p_image_right, p_image_right, 200, 255, CV_THRESH_BINARY);

    cv::Mat p_image_right = cv::imread("feature/coordinates/right.png",cv::IMREAD_GRAYSCALE);
    cv::threshold(p_image_right,p_image_right,200,255,CV_THRESH_BINARY);

    find_list =  Tools::cv_comparehits_bin_min(sub_image_gray,p_image_right,3);

    if(find_list.count() < 1) return;
    int right_x = find_list[0].x;
    //qDebug()<<"right_x:"<< right_x;



    QList<Result_Feature_Info> RFI;


    //#匹配地图名字
    settings.beginGroup("names");
    QStringList names_keys = settings.childKeys();
    for(int i = 0 ; i< names_keys.count() ;i++){
        //IplImage* p_image = cvLoadImage((QString("feature/coordinates/")+names_keys[i]).toStdString().c_str(),CV_LOAD_IMAGE_GRAYSCALE);
        //cvThreshold(p_image, p_image, 200, 255, CV_THRESH_BINARY);
        cv::Mat p_image = cv::imread((QString("feature/coordinates/")+names_keys[i]).toStdString().c_str(),cv::IMREAD_GRAYSCALE);
        cv::threshold(p_image,p_image,200,255,CV_THRESH_BINARY);
        find_list.clear();
        find_list =  Tools::cv_comparehits_bin_min(sub_image_gray,p_image,2,0,left_x);

        foreach(Find_Obj_Result result, find_list){
            RFI.append({result,settings.value(names_keys[i]).toString()});
        }
    }
    settings.endGroup();

    //#匹配坐标
    settings.beginGroup("numbers");
    QStringList numbers_keys = settings.childKeys();
    for(int i = 0 ; i< numbers_keys.count() ;i++){
        //IplImage* p_image = cvLoadImage((QString("feature/coordinates/")+numbers_keys[i]).toStdString().c_str(),CV_LOAD_IMAGE_GRAYSCALE);
        //cvThreshold(p_image, p_image, 200, 255, CV_THRESH_BINARY);
        cv::Mat p_image = cv::imread((QString("feature/coordinates/")+numbers_keys[i]).toStdString().c_str(),cv::IMREAD_GRAYSCALE);
        cv::threshold(p_image,p_image,200,255,CV_THRESH_BINARY);
        find_list.clear();
        find_list =  Tools::cv_comparehits_bin_min(sub_image_gray,p_image,2,left_x,0);

        foreach(Find_Obj_Result result, find_list){
            RFI.append({result,settings.value(numbers_keys[i]).toString()});
        }
    }
    settings.endGroup();


    if (RFI.count()<1) return;
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
    if(ls.count()>0)
        this->MapName = ls[0];
    if(ls.count()>1)
        ls = ls[1].split(']');

        if(ls.count()>1)
            ls = ls[0].split('@');
            if(ls.count()>1){
                this->HeroLocation.setX(ls[0].toInt());
                this->HeroLocation.setY(ls[1].toInt());
            }

}

void MainWindow::find_minimapmouse_location(cv::Mat &Ipl_image)
{
    QPoint minimap ={-1,-1};
    if(this->MousePoint.x() < 0 || this->MousePoint.x() < 0) {
        this->MinimapmouseLocation.setX(-1);
        this->MinimapmouseLocation.setY(-1);
        return ;
    }

    minimap = minimapmouse_location_sub(Ipl_image,0);
    if(minimap.x() > 0){

    }else{
        minimap = minimapmouse_location_sub(Ipl_image,1);

    }


    this->MinimapmouseLocation.setX(minimap.x());
    this->MinimapmouseLocation.setY(minimap.y());

}

QPoint MainWindow::minimapmouse_location_sub(cv::Mat &Ipl_image, int type)
{
    QPoint minimap ={-1,-1};

    int startx = this->MousePoint.x()-34;
    int starty = this->MousePoint.y()-26-5;

    if(type == 1){
        startx = this->MousePoint.x()-34;
        starty = this->MousePoint.y()+27;
    }


    if(startx < 0 || starty<0) return minimap;
    if(startx+68 > Ipl_image.cols || starty+26 >Ipl_image.rows ) return minimap;


    QSettings settings("feature/minimaplocation/minimaplocation.ini", QSettings::IniFormat);

    cv::Mat sub_image = Tools::cvGetSubImage(Ipl_image,cv::Rect(startx,starty ,68,26));

    cv::Mat sub_image_gray =cv::Mat(sub_image.rows,sub_image.cols,CV_8UC1);

    cv::cvtColor(sub_image,sub_image_gray,CV_BGR2GRAY);

    cv::threshold(sub_image_gray,sub_image_gray,200,255,CV_THRESH_BINARY);

    QList<Find_Obj_Result> find_list;

    QList<Result_Feature_Info> RFI;


    //#匹配坐标
    settings.beginGroup("numbers");
    QStringList numbers_keys = settings.childKeys();
    for(int i = 0 ; i< numbers_keys.count() ;i++){

        cv::Mat p_image = cv::imread((QString("feature/minimaplocation/")+numbers_keys[i]).toStdString().c_str(),cv::IMREAD_GRAYSCALE);
        cv::threshold(p_image,p_image,200,255,CV_THRESH_BINARY);
        find_list.clear();
        find_list =  Tools::cv_comparehits_bin_min_x(sub_image_gray,p_image,cv::Mat(),1,0,0);

        foreach(Find_Obj_Result result, find_list){
            RFI.append({result,settings.value(numbers_keys[i]).toString()});
        }
    }
    settings.endGroup();

    if(RFI.count() < 3) return minimap;
    //排序
    qSort(RFI.begin(),RFI.end(),
          [](Result_Feature_Info x,Result_Feature_Info y)->bool{
            return x.fresult.x < y.fresult.x;
    });



    QString str_location;
    foreach(Result_Feature_Info rf,RFI ){
        str_location+=rf.mean;
    }


    QStringList ls = str_location.split('@');

    if(ls.count()==2){
        minimap = {ls[0].toInt(),ls[1].toInt()};
    }

    return minimap;
}

void MainWindow::map_info_update()
{
    QSettings settings("feature/map/mapsizeinfo.ini", QSettings::IniFormat);
    settings.setIniCodec("UTF8");
    settings.beginGroup("Basic");
    QStringList numbers_keys = settings.childKeys();
    for(int i = 0 ; i< numbers_keys.count() ;i++){
        QStringList str_value = settings.value(numbers_keys[i]).toString().split('@');
        if(this->MapName.compare(str_value[0]) == 0){
            this->MapSize={str_value[1].toInt(),str_value[2].toInt()};
            this->MiniMapSize={str_value[3].toInt(),str_value[4].toInt()};
            break;
        }
    }
}

void MainWindow::ui_heroinfo_update()
{
    QString str = QString("鼠标:[%1,%2]").arg(this->MousePoint.x()).arg(this->MousePoint.y());
    this->ui->l_MousePoint->setText(str);

    str = QString("人物坐标:[%1,%2]").arg(this->HeroLocation.x()).arg(this->HeroLocation.y());
    this->ui->l_HeroPoint->setText(str);

    str = QString("地图名称:%1").arg(this->MapName);
    this->ui->l_MapName->setText(str);

    str = QString("坐标:[%1,%2]").arg(this->MinimapmouseLocation.x()).arg(this->MinimapmouseLocation.y());
    this->ui->l_MiniMap_Point->setText(str);

    str = QString("MiniMapSize:[%1,%2]").arg(this->MiniMapSize.width()).arg(this->MiniMapSize.height());
    this->ui->l_MiniMap_Size->setText(str);

    str = QString("Size:[%1,%2]").arg(this->MapSize.width()).arg(this->MapSize.height());
    this->ui->l_Map_Size->setText(str);
}









//##############################property


QList<int> MainWindow::getMousePoint()
{
    QList<int> value ={this->MousePoint.x(),this->MousePoint.y()};
    return value;
}

QString MainWindow::getMapName()
{
    return this->MapName;

}

QList<int> MainWindow::getMapSize()
{
    QList<int> value ={this->MapSize.width(),this->MapSize.height()};
    return value;
}

QList<int> MainWindow::getMiniMapSize()
{
    QList<int> value ={this->MiniMapSize.width(),this->MiniMapSize.height()};
    return value;
}

QList<int> MainWindow::getHeroLocation()
{

    QList<int> value ={this->HeroLocation.x(),this->HeroLocation.y()};
    return value;
}

QList<int> MainWindow::getMinimapmouseLocation()
{
    QList<int> value ={this->MinimapmouseLocation.x(),this->MinimapmouseLocation.y()};
    return value;
}

QList<int> MainWindow::getTempValueList()
{
    return TempValueList;
}

