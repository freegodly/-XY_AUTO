import opencv.imgproc, opencv.highgui, opencv.core
import times, strutils, os
import glib2, gtk2

import Tools

# proc destroy(widget: PWidget, data: Pgpointer) {.cdecl.} =
#   main_quit()
#
# var
#   window: PWidget
# nimrod_init()
# window = window_new(WINDOW_TOPLEVEL)
# discard signal_connect(window, "destroy",
#                        SIGNAL_FUNC(main.destroy), nil)
# show(window)
# main()


#echo "aahahah"
var p_image = loadImage("img/bg1.png",LOAD_IMAGE_COLOR)
var p_image_mouse = loadImage("feature/other/mouse.png",LOAD_IMAGE_COLOR)
var p_image_mouse_mask = loadImage("feature/other/mouse_mask.png",LOAD_IMAGE_GRAYSCALE)
var t = cpuTime()
var find = find_obj_hist_mask(p_image,p_image_mouse,p_image_mouse_mask,
            max_sum=255,move_px = 5,move_py=5)
echo find
echo "Time taken: ",cpuTime() - t
discard namedWindow("xxx",WINDOW_AUTOSIZE)
showImage("xxx",p_image)
discard waitKey(0)
