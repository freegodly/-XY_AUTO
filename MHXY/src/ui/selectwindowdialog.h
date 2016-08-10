#ifndef SELECTWINDOWDIALOG_H
#define SELECTWINDOWDIALOG_H

#include <QDialog>
#include <windows.h>
#include "../Tools/tools.h"

namespace Ui {
class SelectWindowDialog;
}

class SelectWindowDialog : public QDialog
{
    Q_OBJECT

public:
    explicit SelectWindowDialog(QWidget *parent = 0);
    ~SelectWindowDialog();

public:
    HWND Select_Hwnd;

private slots:
    void on_listWidget_WindowList_doubleClicked(const QModelIndex &index);

private:
    Ui::SelectWindowDialog *ui;
    QList<Window_Info> wil;
};

#endif // SELECTWINDOWDIALOG_H
