#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QScreen>
#include <QWindow>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QScreen *screen = QGuiApplication::primaryScreen();
    if (const QWindow *window = windowHandle())
        screen = window->screen();
    if (!screen)
      return;



    originalPixmap = screen->grabWindow(0);
    this->ui->GameRect->setPixmap(originalPixmap.scaled(this->ui->GameRect->size(),
                                                           Qt::KeepAspectRatio,
                                                           Qt::SmoothTransformation));
}

MainWindow::~MainWindow()
{
    delete ui;
}
