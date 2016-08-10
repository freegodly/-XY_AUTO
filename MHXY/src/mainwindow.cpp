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






MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
   IsRunScript  = false;
   timer_status = false;
   this->imgData = new uchar[640*480*3];

   GameHwnd = FindWindowA("WSGAME",NULL);
   QScriptValue qcmu = engine.newQObject(this);
   engine.globalObject().setProperty("XY", qcmu);

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

        QPixmap Game_originalPixmap=screen->grabWindow(QApplication::desktop()->winId(),rect.left+3,rect.top+26,640,480);

        QImage image = Game_originalPixmap.toImage();

        IplImage* Ipl_sub_image = Tools::QImageToIplImage(&image);


        find_obj(Ipl_sub_image);


        map_info_update();
        ui_heroinfo_update();


        //给dorun使用
        this->p_Game_Image = Ipl_sub_image;
        PaintRectList.clear();

        if(IsRunScript)
        {
            engine.evaluate("dorun();");
            if(engine.hasUncaughtException()){

                    QString errinfo =  engine.uncaughtException().toString();
                    errinfo += engine.uncaughtExceptionBacktrace().join("/n");

                    Add_Log_Msg(errinfo);
            }
        }


        cvReleaseImage(&Ipl_sub_image);


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

        painter.end();

        this->ui->GameRect->setPixmap(Game_originalPixmap);









    }
}

void MainWindow::Add_Log_Msg(QString msg)
{
    ui->t_RunLog->append(msg);
}

void MainWindow::Clear_Log_Msg()
{
    ui->t_RunLog->clear();
}

void MainWindow::Mouse_Move_To(int x, int y)
{
    hardKeyMouse.MouseMove(this->GameRect.left()+x,this->GameRect.top()+y);
}

void MainWindow::Mouse_Click(int type)
{
    hardKeyMouse.MouseClick(type);
}

void MainWindow::Key_Click(int key1, int key2)
{
    hardKeyMouse.KeyClick(key1,key2);
}

QList<int> MainWindow::Match_Image_Rect(QString image_name, float mini_value, int method)
{
    QList<int> qrect={-1,-1,0,0};

    IplImage* p_image_mouse = cvLoadImage(image_name.toStdString().c_str(),CV_LOAD_IMAGE_COLOR);

    if(p_image_mouse != NULL) {
        CvRect rect=  Tools::find_obj_matchtemplate(this->p_Game_Image,p_image_mouse,mini_value,method);
        cvReleaseImage(&p_image_mouse);
        qrect = {rect.x,rect.y,rect.width,rect.height};
    }

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
    PaintRectList.append({x,y,w,h});
}

void MainWindow::on_pushButton_Test_clicked()
{

}

void MainWindow::on_actionStart_triggered()
{
    if(!timer_status){
        this->timer_id = this->startTimer(150);
        timer_status = true;
    }

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

            Add_Log_Msg(errinfo);
    }
}

void MainWindow::on_actionStop_triggered()
{
    this->killTimer(this->timer_id);
    timer_status = false;
}


void MainWindow::find_obj(IplImage* Ipl_image)
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

void MainWindow::find_mouse_location(IplImage *Ipl_image)
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
    IplImage* p_image_mouse = cvLoadImage("feature/other/mouse_s.png",CV_LOAD_IMAGE_COLOR);

    CvRect rect=  Tools::find_obj_matchtemplate(Ipl_image,p_image_mouse,0.97,1);

    cvReleaseImage(&p_image_mouse);

    this->MousePoint.setX(rect.x-10);
    this->MousePoint.setY(rect.y-10);

}

void MainWindow::find_hero_location(IplImage *Ipl_image)
{
    QSettings settings("feature/coordinates/coordinates.ini", QSettings::IniFormat);
    settings.setIniCodec("UTF8");

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
    //qDebug()<<"left_x:"<< left_x;

    find_list.clear();
    IplImage* p_image_right = cvLoadImage("feature/coordinates/right.png",CV_LOAD_IMAGE_GRAYSCALE);
    cvThreshold(p_image_right, p_image_right, 200, 255, CV_THRESH_BINARY);
    find_list =  Tools::comparehits_bin_min(sub_image_gray,p_image_right,3);
    cvReleaseImage(&p_image_right);
    if(find_list.count() < 1) return;
    int right_x = find_list[0].x;
    //qDebug()<<"right_x:"<< right_x;



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
            RFI.append({result,settings.value(names_keys[i]).toString()});
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

void MainWindow::find_minimapmouse_location(IplImage *Ipl_image)
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

QPoint MainWindow::minimapmouse_location_sub(IplImage *Ipl_image, int type)
{
    QPoint minimap ={-1,-1};

    int startx = this->MousePoint.x()-34;
    int starty = this->MousePoint.y()-26-5;

    if(type == 1){
        startx = this->MousePoint.x()-34;
        starty = this->MousePoint.y()+27;
    }


    if(startx < 0 || starty<0) return minimap;
    if(startx+68 > Ipl_image->width || starty+26 >Ipl_image->height ) return minimap;


    QSettings settings("feature/minimaplocation/minimaplocation.ini", QSettings::IniFormat);

    IplImage* sub_image = Tools::GetSubImage(Ipl_image,cvRect(startx,starty ,68,26));
    IplImage *  sub_image_gray = cvCreateImage(CvSize(sub_image->width,sub_image->height),sub_image->depth,1);

    cvCvtColor(sub_image,sub_image_gray,CV_BGR2GRAY); //关键

    cvThreshold(sub_image_gray, sub_image_gray, 200, 255, CV_THRESH_BINARY);


    QList<Find_Obj_Result> find_list;

    QList<Result_Feature_Info> RFI;


    //#匹配坐标
    settings.beginGroup("numbers");
    QStringList numbers_keys = settings.childKeys();
    for(int i = 0 ; i< numbers_keys.count() ;i++){
        IplImage* p_image = cvLoadImage((QString("feature/minimaplocation/")+numbers_keys[i]).toStdString().c_str(),CV_LOAD_IMAGE_GRAYSCALE);
        cvThreshold(p_image, p_image, 200, 255, CV_THRESH_BINARY);
        find_list.clear();
        find_list =  Tools::comparehits_bin_min_x(sub_image_gray,p_image,NULL,1,0,0);
        cvReleaseImage(&p_image);
        foreach(Find_Obj_Result result, find_list){
            RFI.append({result,settings.value(numbers_keys[i]).toString()});
        }
    }
    settings.endGroup();

    //释放资源
    cvReleaseImage(&sub_image);
    cvReleaseImage(&sub_image_gray);

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








///////////////////////////////property


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


void MainWindow::on_action_ScriptRun_triggered()
{
    IsRunScript = true;
}

void MainWindow::on_action_ScriptStop_triggered()
{
     IsRunScript = false;
}

void MainWindow::on_action_LoadScript_triggered()
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

            Add_Log_Msg(errinfo);
    }
}

void MainWindow::on_actionSelectWindow_triggered()
{


    SelectWindowDialog swd;
    swd.exec();
    GameHwnd = swd.Select_Hwnd;
    qDebug()<<GameHwnd;
}
