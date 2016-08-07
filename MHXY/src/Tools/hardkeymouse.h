#ifndef HARDKEYMOUSE_H
#define HARDKEYMOUSE_H

#include <QObject>
#include <QLibrary>

class HardKeyMouse : public QObject
{
    Q_OBJECT
public:
    explicit HardKeyMouse(QObject *parent = 0);
    void KeyClick(int key1, int key2);
    void MouseClick(int button);
    void MouseMove(int x,int y);
signals:

public slots:

private:
   static QLibrary *dd;
};

#endif // HARDKEYMOUSE_H
