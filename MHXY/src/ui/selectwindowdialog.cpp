#include "selectwindowdialog.h"
#include "ui_selectwindowdialog.h"

SelectWindowDialog::SelectWindowDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::SelectWindowDialog)
{
    ui->setupUi(this);

    wil = Tools::GetTopWindow();
    Select_Hwnd = NULL;

    foreach(Window_Info wi,wil){

        ui->listWidget_WindowList->addItem(wi.Title);
    }
}

SelectWindowDialog::~SelectWindowDialog()
{
    delete ui;
}

void SelectWindowDialog::on_listWidget_WindowList_doubleClicked(const QModelIndex &index)
{

   Select_Hwnd = wil.at(index.row()).hwnd;
   this->close();
}
