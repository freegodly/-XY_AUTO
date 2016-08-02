
import opencv.imgproc, opencv.highgui, opencv.core

proc find_obj_hist_mask*(trainImage:ptr TIplImage,
                        queryImage:ptr TIplImage,
                        mask:ptr TIplImage = nil,
                        max_sum:float=20,
                        bins:int = 30,
                        startx:int = 0 ,endx:int = 0,
                        starty:int = 0 ,endy:int = 0,
                        move_px:int = 1,move_py:int = 1):tuple[x: int, y: int,error: float]  =
    echo getSize(queryImage)
    echo getSize(mask)
    var
        w = trainImage.width
        h = trainImage.height
        h_f = queryImage.height
        w_f = queryImage.width

    var
        start_px = -1
        start_py = -1
        my_endx  = endx
        my_endy  = endy
        bins_size :array[0..1,cint]
    bins_size[0] = cast[cint](bins)
    if my_endx==0 :
        my_endx = w
    if my_endy==0 :
        my_endy = h

    var
        queryImage_b = createImage(size(w_f,h_f),queryImage.depth,1)
        queryImage_g = createImage(size(w_f,h_f),queryImage.depth,1)
        queryImage_r = createImage(size(w_f,h_f),queryImage.depth,1)

        queryImage_b_hist = createHist(1,bins_size[0].addr(),HIST_ARRAY)
        queryImage_g_hist = createHist(1,bins_size[0].addr(),HIST_ARRAY)
        queryImage_r_hist = createHist(1,bins_size[0].addr(),HIST_ARRAY)


        trainImage_b = createImage(size(w_f,h_f),queryImage.depth,1)
        trainImage_g = createImage(size(w_f,h_f),queryImage.depth,1)
        trainImage_r = createImage(size(w_f,h_f),queryImage.depth,1)

        trainImage_b_hist = createHist(1,bins_size[0].addr(),HIST_ARRAY)
        trainImage_g_hist = createHist(1,bins_size[0].addr(),HIST_ARRAY)
        trainImage_r_hist = createHist(1,bins_size[0].addr(),HIST_ARRAY)



    split(queryImage,queryImage_b,queryImage_g,queryImage_r,nil)
    calcHist(queryImage_b.addr(),queryImage_b_hist,mask=mask)
    calcHist(queryImage_g.addr(),queryImage_g_hist,mask=mask)
    calcHist(queryImage_r.addr(),queryImage_r_hist,mask=mask)
    # normalizeHist(trainImage_b_hist,1.0)
    # normalizeHist(queryImage_g_hist,1.0)
    # normalizeHist(queryImage_r_hist,1.0)
    var min_error :cdouble = max_sum
    var result :tuple[x: int, y: int,error: float] = (-1,-1,-1.0)
    for j in countup(0, int((my_endy-starty-h_f)/move_py) ):
        start_py = j*move_py+starty
        for i in countup(0, int((my_endx-startx-w_f)/move_px) ):
            start_px = i*move_px+startx
            setImageROI(trainImage,rect(cint(start_px),cint(start_py),w_f,h_f))
            split(trainImage,trainImage_b,trainImage_g,trainImage_r,nil)
            calcHist(trainImage_b.addr(),trainImage_b_hist,mask=mask)
            calcHist(trainImage_g.addr(),trainImage_g_hist,mask=mask)
            calcHist(trainImage_r.addr(),trainImage_r_hist,mask=mask)
            resetImageROI(trainImage)

            # normalizeHist(trainImage_b_hist,1.0)
            # normalizeHist(trainImage_g_hist,1.0)
            # normalizeHist(trainImage_r_hist,1.0)

            var now_error = 0.0
            now_error = now_error + compareHist(queryImage_b_hist,trainImage_b_hist,COMP_CHISQR)
            now_error = now_error + compareHist(queryImage_g_hist,trainImage_g_hist,COMP_CHISQR)
            now_error = now_error + compareHist(queryImage_r_hist,trainImage_r_hist,COMP_CHISQR)

            if now_error < min_error :
                min_error = now_error
                result =  (start_px,start_py,min_error)

    releaseHist(queryImage_b_hist.addr())
    releaseHist(queryImage_g_hist.addr())
    releaseHist(queryImage_r_hist.addr())
    releaseHist(trainImage_b_hist.addr())
    releaseHist(trainImage_g_hist.addr())
    releaseHist(trainImage_r_hist.addr())

    releaseImage(queryImage_b.addr())
    releaseImage(queryImage_g.addr())
    releaseImage(queryImage_r.addr())
    releaseImage(trainImage_b.addr())
    releaseImage(trainImage_g.addr())
    releaseImage(trainImage_r.addr())


    return result
