opencv中有两个函数可以训练分类器opencv_haartraining.exe和opencv_traincascade.exe,前者只能训练haar特征，后者可以用HAAR、LBP和HOG特征训练分类器。这两个函数都可以在opencv\build\x86\vc10\bin文件夹下找到，opencv_haartraining.exe训练的adaboost级联分类器有很多了，本文主要讲opencv_haartraining.exe训练的LBP和HOG特征的分类器。

训练的过程包过四步：

首先是样本的准备、其次是对样本进行处理、再次生成样本描述文件、最后一步是训练分类器。

1、样本的准备

以行人训练为例，首先正样本是各种各样的行人的照片，负样本就是非人照片。样本个数最好在上千个，个数太少训练出来的分类器不能准确的检测行人，网上对正负样本的个数比例不尽相同，有的说3:1有的说7:3,具体的还是要自己去实验，我用的正样本有2000个负样本1200个。把正负样本分别放在不同的文件夹下，可以命名为pos、neg。同时也要把opencv自带的训练函数和正负样本一起放到一个文件夹下，例如放到E盘的boost文件夹下。如图

用opencv的traincascade.exe训练行人的HAAR、LBP和HOG特征的xml

这样就准备好了正负样本了。
ps：对正负样本的几点说明。。。

正负样本都要转化成灰度图，而且对于正样本用haar特征训练是规格化成20*20或其他大小，最好不要太大，过多的haar特征会影响分类器的训练时间；对于LBP特征正样本要规格化为24*24大小，而对于HOG要规格化成64*64. 负样本对尺寸没有统一要求，在训练对应的分类器时，选择的负样本尺寸一定要大于等于正样本规定的尺寸。                   a，正样本就是人的图片就行了，尽量包含少的背景。     b，，负样本有两点要求：一，不能包含正样本且尽可能多的提供场景的背景图；二，负样本尽可能的多，而且要多样化，和正样本有一定的差距但是差别也不要太大，否则容易在第一级就全部被分类器reject，训练时不能显示负样本的个数，从而导致卡死。

2、对样本进行处理

以下的处理过程都是在命令行下进行的，在计算机【开始】里面输入“cmd”就可以进入命令行了。。。。。。

然后进入你刚才新建的包含以上样本的文件夹下  首先进入E盘 直接输入E：就可以了，其次输入“cd boost”就可以进入刚才的文件夹下。输入“CD..”可以返回上一程

用opencv的traincascade.exe训练行人的HAAR、LBP和HOG特征的xml

输入dir /b >pos.txt 可以在pos文件夹下生成正样本描述文件，文件是txt文件，包含的内容是正样本中图片的对应序号和格式。把其中的格式jpg改成jpg 1 0 0 24 24

用opencv的traincascade.exe训练行人的HAAR、LBP和HOG特征的xml

后面的0 0 24 24是你规格化图片的大小，即矩形框的大小，和你自己规格化的正样本图片大小要保持一致。全部替换以后，再把最后一行的pos.txt删除就可以了。对于负样本，以上生成方式一样，不需要对txt文件的图片格式进行修改，只需要删除最后一行的neg.txt即可。这样正负样本就处理好了。。。
3、生成样本描述文件

对正负样本进行以上预处理之后，就可以创建正样本vec文件了。

命令行进入opencv_createsamples.exe文件夹下，依次输入：opencv_createsamples.exe -info pos\pos.txt -vec pos.vec -bg neg\neg.txt -num 2000 -w 24 -h 24 回车之后文件夹下就会出现pos.vec文件。

用opencv的traincascade.exe训练行人的HAAR、LBP和HOG特征的xml


以上参数的含义如下：
－vec <vec_file_name>：训练好的正样本的输出文件名。
－img<image_file_name>：源目标图片（例如：一个公司图标）
－bg<background_file_name>：背景描述文件。
－num<number_of_samples>：要产生的正样本的数量，和正样本图片数目相同。
－bgcolor<background_color>：背景色（假定当前图片为灰度图）。背景色制定了透明色。对于压缩图片，颜色方差量由bgthresh参数来指定。则在bgcolor－bgthresh 和bgcolor＋bgthresh 中间的像素被认为是透明的。
－bgthresh<background_color_threshold>

－inv：如果指定，颜色会反色
－randinv：如果指定，颜色会任意反色
－maxidev<max_intensity_deviation>：背景色最大的偏离度。
－maxangel<max_x_rotation_angle>，
－maxangle<max_y_rotation_angle>，
－maxzangle<max_x_rotation_angle>：最大旋转角度，以弧度为单位。
－show：如果指定，每个样本会被显示出来，按下"esc"会关闭这一开关，即不显示样本图片，而创建过程
继续。这是个有用的debug 选项。
－w<sample_width>：输出样本的宽度（以像素为单位）
－h<sample_height>：输出样本的高度（以像素为单位）

只需要对正样本进行以上操作，负样本不需要生成vec文件。。。
4、训练分类器

在以上准备工作都做好的情况下，就可以进行训练分类器了。

在cmd命令行下输入：opencv_traincascade.exe -data xml -vec pos.vec -bg neg\neg.txt -numpos 1800 -numneg 1200 -numstages 20 -featureType LBP -w 24 -h 24