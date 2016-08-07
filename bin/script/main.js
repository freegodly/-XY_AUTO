/*******************************************************************

Q_PROPERTY( QPoint      MousePoint              READ getMousePoint)
Q_PROPERTY( QString     MapName                 READ getMapName)
Q_PROPERTY( QSize       MapSize                 READ getMapSize)
Q_PROPERTY( QSize       MiniMapSize             READ getMiniMapSize)
Q_PROPERTY( QPoint      HeroLocation            READ getHeroLocation)
Q_PROPERTY( QPoint      MinimapmouseLocation    READ getMinimapmouseLocation)


void Add_Log_Msg(QString msg);

void Clear_Log_Msg();

void Mouse_Move_To(int x , int y);

void Mouse_Click(int type);

void Key_Click(int key1,int key2=-1);

QRect Match_Image_Rect(QString image_name,float mini_value = 0.8,int method);

void Set_Gamge_ForegroundWindow();

void Draw_Gamge_Rect(int x,int y,int w,int h);
***********************************************************************/


var MapSwitchInfo =[	
	{
		"from":"长安城",
		"to":"江南野外",
		"gopoint":[537,3],
		"mousemove":[590,360],
		"switchconfirm":false,
		"npc_image":"",
	},
	{
		"from":"江南野外",
		"to":"长安城",
		"gopoint":[20,109],
		"mousemove":[190,43],
		"switchconfirm":false,
		"npc_image":"",
	},
	{
		"from":"江南野外",
		"to":"建邺城",
		"gopoint":[143,60],
		"mousemove":[569,227],
		"switchconfirm":false,
		"npc_image":"",
	},
	{
		"from":"建邺城",
		"to":"江南野外",
		"gopoint":[20,8],
		"mousemove":[156,341],
		"switchconfirm":true,
		"npc_image":"",
	},
	{
		"from":"建邺城",
		"to":"东海湾",
		"gopoint":[268,27],
		"mousemove":[593,302],
		"switchconfirm":false,
		"npc_image":"",
	},
	{
		"from":"东海湾",
		"to":"建邺城",
		"gopoint":[12,4],
		"mousemove":[13,400],
		"switchconfirm":false,
		"npc_image":"",
	},
	{
		"from":"东海湾",
		"to":"傲来国",
		"gopoint":[56,21],
		"mousemove":[-1,-1],
		"switchconfirm":true,
		"npc_image":"feature/map/to_aolai.png",
	},
	{
		"from":"傲来国",
		"to":"东海湾",
		"gopoint":[165,16],
		"mousemove":[-1,-1],
		"switchconfirm":true,
		"npc_image":"feature/map/to_dohaiwan.png",
	},
	{
		"from":"傲来国",
		"to":"花果山",
		"gopoint":[207,139],
		"mousemove":[600,165],
		"switchconfirm":false,
		"npc_image":"",
	},
	{
		"from":"花果山",
		"to":"傲来国",
		"gopoint":[13,8],
		"mousemove":[15,303],
		"switchconfirm":false,
		"npc_image":"",
	},
	{
		"from":"花果山",
		"to":"北俱芦洲",
		"gopoint":[35,96],
		"mousemove":[187,176],
		"switchconfirm":true,
		"npc_image":"",
	},
	{
		"from":"北俱芦洲",
		"to":"花果山",
		"gopoint":[186,105],
		"mousemove":[491,224],
		"switchconfirm":true,
		"npc_image":"",
	},
	{
		"from":"北俱芦洲",
		"to":"长寿郊外",
		"gopoint":[189,6],
		"mousemove":[431,369],
		"switchconfirm":true,
		"npc_image":"",
	},
	{
		"from":"长寿郊外",
		"to":"北俱芦洲",
		"gopoint":[66,64],
		"mousemove":[206,161],
		"switchconfirm":true,
		"npc_image":"",
	},
	{
		"from":"长寿郊外",
		"to":"长寿村",
		"gopoint":[153,157],
		"mousemove":[342,5],
		"switchconfirm":false,
		"npc_image":"",
	},
		{
		"from":"长寿村",
		"to":"长寿郊外",
		"gopoint":[140,7],
		"mousemove":[494,414],
		"switchconfirm":false,
		"npc_image":"",
	},
]






var TaskState = new Array();

var TaskList = new Array();

TaskState.Run_Times = 0;
TaskState.NowRunTaskIndex = 0;
TaskState.CellTaskState =  new Array();


//[x,y]
function GoPointMiniMap(Args,CellTaskState){
	CellTaskState.GoPoint = Args
	if(CellTaskState.NowRun == null){
		XY.Add_Log_Msg("GoPointMiniMap.....Start");
		CellTaskState.NowRun = GoPointMiniMap;
		CellTaskState.RunStep = 0
		CellTaskState.RunInit = false
		CellTaskState.PerHeroLocation = [-1,-1]
		XY.Mouse_Move_To(320,240);
		XY.Key_Click(300,-1);
		return false;
	}
	//判断鼠标是否到达中心位置
	if(!CellTaskState.RunInit){
		if(Math.abs(320-XY.MousePoint[0]) < 50 && Math.abs(240-XY.MousePoint[1])<50){
			
			if(Math.abs(CellTaskState.PerHeroLocation[0]-XY.HeroLocation[0]) < 2 &&
			 Math.abs(CellTaskState.PerHeroLocation[1]-XY.HeroLocation[1])<2){
				CellTaskState.RunInit = true;
			}
			
		}
		CellTaskState.PerHeroLocation = XY.HeroLocation
		return false
	}


	var x_diff = CellTaskState.GoPoint[0]-XY.MinimapmouseLocation[0]
    var y_diff = XY.MinimapmouseLocation[1]-CellTaskState.GoPoint[1]

	if(Math.abs(x_diff) <2 && Math.abs(y_diff) <2)
	{
		var hero_x_diff = CellTaskState.GoPoint[0]-XY.HeroLocation[0]
    	var hero_y_diff = XY.HeroLocation[1]-CellTaskState.GoPoint[1]
		if(Math.abs(hero_x_diff) <3 && Math.abs(hero_y_diff) <3)
		{
			//到达目标位置
			XY.Key_Click(300,-1);
			XY.Add_Log_Msg("GoPointMiniMap.....OK");
			return true;
		}
		else
		{
			XY.Mouse_Click(0);
			return false;
		}
		
	}
	else
	{
	 	x_diff = CellTaskState.GoPoint[0]-XY.MinimapmouseLocation[0]
		y_diff = XY.MinimapmouseLocation[1]-CellTaskState.GoPoint[1]
		XY.Add_Log_Msg("X:"+x_diff+"  Y:"+y_diff)

		if(XY.MinimapmouseLocation[0] < 1 ||  XY.MousePoint[0] < 1) {
			return false;
		}
		else if(CellTaskState.RunStep == 0) {
			XY.Add_Log_Msg("Start_MinimapmouseLocation:"+XY.MinimapmouseLocation);
			XY.Add_Log_Msg("Start_MouseLocation:"+XY.MousePoint);
			CellTaskState.Start_MinimapmouseLocation = XY.MinimapmouseLocation;
			CellTaskState.Start_MouseLocation = XY.MousePoint;
			CellTaskState.RunStep = 1;
			return false;
		}
		else if(CellTaskState.RunStep == 1){
			XY.Mouse_Move_To(340,260);
			if(Math.abs(340-XY.MousePoint[0]) < 50 && Math.abs(260-XY.MousePoint[1])<50){
				CellTaskState.RunStep = CellTaskState.RunStep  + 1 ;
			}
			
			return false;
		}
		else if(CellTaskState.RunStep == 2) {
			XY.Add_Log_Msg("Test_MinimapmouseLocation:"+XY.MinimapmouseLocation);
			XY.Add_Log_Msg("Test_MouseLocation:"+XY.MousePoint);
			CellTaskState.Test_MinimapmouseLocation = XY.MinimapmouseLocation;
			CellTaskState.Test_MouseLocation = XY.MousePoint;

			CellTaskState.Scale_X = (CellTaskState.Test_MinimapmouseLocation[0]-CellTaskState.Start_MinimapmouseLocation[0])*1.0/
									(CellTaskState.Test_MouseLocation[0]-CellTaskState.Start_MouseLocation[0]);
			CellTaskState.Scale_X = Math.abs(CellTaskState.Scale_X)
			CellTaskState.Scale_Y = (CellTaskState.Test_MinimapmouseLocation[1]-CellTaskState.Start_MinimapmouseLocation[1])*1.0/
									(CellTaskState.Test_MouseLocation[1]-CellTaskState.Start_MouseLocation[1]);
			CellTaskState.Scale_Y = Math.abs(CellTaskState.Scale_Y)	
			CellTaskState.RunStep = CellTaskState.RunStep  + 1 ;


			XY.Add_Log_Msg("Scale_X:"+CellTaskState.Scale_X+"  Scale_Y:"+CellTaskState.Scale_Y)

			CellTaskState.Start_MouseLocation = XY.MousePoint;
			return false;
		}
		else if(CellTaskState.RunStep%2 == 0) {
		    // var mov_x = parseInt(x_diff*(XY.MiniMapSize[0]*1.0/XY.MapSize[0]))/3 
		    // var mov_y = parseInt(y_diff*(XY.MiniMapSize[1]*1.0/XY.MapSize[1]))/3
	      	var mov_x = x_diff*CellTaskState.Scale_X/2
		    var mov_y = y_diff*CellTaskState.Scale_Y/2

		    if(mov_x > 0 && mov_x<1) mov_x=1
	    	else if(mov_x < 0 && mov_x>-1) mov_x = -1
	    	else	mov_x = parseInt(mov_x)

	    	if(mov_y > 0 && mov_y<1) mov_y=1
	    	else if(mov_y < 0 && mov_y>-1) mov_y = -1
	    	else	mov_y = parseInt(mov_y)

		    XY.Mouse_Move_To(CellTaskState.Start_MouseLocation[0]+mov_x,CellTaskState.Start_MouseLocation[1]+mov_y)
		    CellTaskState.Start_MouseLocation =[CellTaskState.Start_MouseLocation[0]+mov_x,CellTaskState.Start_MouseLocation[1]+mov_y];
		    
		    CellTaskState.RunStep = CellTaskState.RunStep  + 1 ;
		    return false;
		}
		else if (CellTaskState.RunStep%2 == 1) {

			CellTaskState.Start_MinimapmouseLocation = XY.MinimapmouseLocation

			CellTaskState.RunStep = CellTaskState.RunStep  + 1 ;
			return false;
		}
	}
}

//[x,y]
function MouseMoveToGameScreen(Args,CellTaskState){
	CellTaskState.GoPoint = Args
	if(CellTaskState.NowRun == null){
		XY.Add_Log_Msg("MouseMoveToGameScreen.....Start");
		CellTaskState.NowRun = MouseMoveToGameScreen;
		CellTaskState.RunStep = 0
		CellTaskState.Point_Diff = [100,100]
		XY.Mouse_Move_To(320,240);
		return false;
	}
	

	if(Math.abs(CellTaskState.Point_Diff[0]) <=3 && Math.abs(CellTaskState.Point_Diff[1]) <=3)
	{
		//到达目标位置
		XY.Add_Log_Msg("MouseMoveToGameScreen.....OK");
		return true;
	}
	else
	{	
		if(XY.MousePoint[0] < 1 ) return false;
		else if(CellTaskState.RunStep == 0) {
			XY.Add_Log_Msg("Start_MouseLocation:"+XY.MousePoint);
			CellTaskState.Start_MouseLocation = XY.MousePoint;
			CellTaskState.RunStep = 1;
			return false;
		}
		else if(CellTaskState.RunStep%2 == 0) {
			
		    var mov_x = parseInt(CellTaskState.Point_Diff[0]*1.0/3)
		    var mov_y = parseInt(CellTaskState.Point_Diff[1]*1.0/3)

		    if(mov_x > 0 && mov_x<1) mov_x=1;
		    if(mov_x < 0 && mov_x>-1) mov_x=-1;
		    if(mov_y > 0 && mov_y<1) mov_y=1;
		    if(mov_y < 0 && mov_y> -1) mov_y=-1;

		    XY.Mouse_Move_To(CellTaskState.Start_MouseLocation[0]+mov_x,CellTaskState.Start_MouseLocation[1]+mov_y)
		    CellTaskState.Start_MouseLocation =[CellTaskState.Start_MouseLocation[0]+mov_x,CellTaskState.Start_MouseLocation[1]+mov_y];
		    
		    CellTaskState.RunStep = CellTaskState.RunStep  + 1 ;
		    return false;
		}
		else{
			CellTaskState.RunStep = CellTaskState.RunStep  + 1 ;

			CellTaskState.Point_Diff=[CellTaskState.GoPoint[0]-XY.MousePoint[0],CellTaskState.GoPoint[1]-XY.MousePoint[1]]
		
			return false;
		}
	}
}

//[srcmap,targmap]
function GoSwitchMap(Args,CellTaskState){
	if(CellTaskState.NowRun == null){
		XY.Add_Log_Msg("GoSwitchMap.....Start");
		CellTaskState.NowRun = GoSwitchMap;
		CellTaskState.RunStep = 0
		CellTaskState.MapSwitchInfoStep = null
		CellTaskState.GoPointMiniMap_TaskState = []
		CellTaskState.MouseMoveToGameScreen_TaskState = []
		CellTaskState.MouseMoveToGameScreen_TaskState_2 = []
		CellTaskState.IsSwitchConfirm = true
		CellTaskState.ConfirmRect =[-1,-1,0,0]
		CellTaskState.MouseMove = [-1,-1]
		for(var i = 0 ; i< MapSwitchInfo.length ; i++){

			var info = MapSwitchInfo[i];
			if(info.from==Args[0] && info.to==Args[1]){
				CellTaskState.MapSwitchInfoStep = info;
				CellTaskState.IsSwitchConfirm = CellTaskState.MapSwitchInfoStep.switchconfirm
				CellTaskState.MouseMove = CellTaskState.MapSwitchInfoStep.mousemove
				break;
			}
		}

		if(CellTaskState.MapSwitchInfoStep == null){
			XY.Add_Log_Msg("未找到相应的地图切换描述信息");
			return true;
		}else{
			XY.Add_Log_Msg("找到地图切换描述信息");
			return false;
		}
	}
	else if(CellTaskState.RunStep == 0){
		if(GoPointMiniMap(CellTaskState.MapSwitchInfoStep.gopoint,CellTaskState.GoPointMiniMap_TaskState)){
			CellTaskState.RunStep=CellTaskState.RunStep+1;
			XY.Key_Click(109,-1)
		}

		return false;
	}
	else if(CellTaskState.RunStep == 1){

		if(CellTaskState.MouseMove[0]<1){
			var ConfirmRect = XY.Match_Image_Rect(CellTaskState.MapSwitchInfoStep.npc_image,0.85,1)
			if(ConfirmRect[0] > 1){
				CellTaskState.MouseMove = [ConfirmRect[0]+ConfirmRect[2]/2,ConfirmRect[1]-50]
				XY.Add_Log_Msg("X:"+ConfirmRect[0]+"  Y:"+ConfirmRect[1])
			}
		}else{
			CellTaskState.RunStep=CellTaskState.RunStep+1;
		}

		return false
	}
	else if(CellTaskState.RunStep == 2){

		if(MouseMoveToGameScreen(CellTaskState.MouseMove,CellTaskState.MouseMove)){
			CellTaskState.RunStep=CellTaskState.RunStep+1;
		}

		return false;
	}
	else if(CellTaskState.RunStep == 3){
		XY.Key_Click(109,-1)
		XY.Mouse_Click(0);
		CellTaskState.RunStep=CellTaskState.RunStep+1;
		return false;
	}
	else if(CellTaskState.RunStep == 4 && CellTaskState.IsSwitchConfirm){
		XY.Mouse_Click(0);
		CellTaskState.ConfirmRect = XY.Match_Image_Rect("feature/map/map_switch_confirm.png",0.95,1)
		if(CellTaskState.ConfirmRect[0] <1){
			//CellTaskState.GoPointMiniMap_TaskState = []
			//CellTaskState.MouseMoveToGameScreen_TaskState = []
			//CellTaskState.RunStep = 0
		}else{
			CellTaskState.RunStep=CellTaskState.RunStep+1;
		}
		
		return false;
	}
	else if(CellTaskState.IsSwitchConfirm && CellTaskState.RunStep == 5){
		
		if(MouseMoveToGameScreen([CellTaskState.ConfirmRect[0]+CellTaskState.ConfirmRect[2]/2,
			CellTaskState.ConfirmRect[1]+CellTaskState.ConfirmRect[3]/2],
			CellTaskState.MouseMoveToGameScreen_TaskState_2))
		{
			CellTaskState.RunStep=CellTaskState.RunStep+1;
			CellTaskState.IsSwitchConfirm = false
			
			XY.Mouse_Click(0);
		}
		
		return false
	}
	else{
		CellTaskState.RunStep=CellTaskState.RunStep+1;
		XY.Mouse_Click(0);
		if(XY.MapName ==CellTaskState.MapSwitchInfoStep.to ){
			XY.Add_Log_Msg("GoSwitchMap.....OK");
			return true;
		}else
		{
			if(CellTaskState.RunStep > 20){
				//重头开始
				CellTaskState.NowRun =null
			}
			return false;
		}
	}
}



function FirstRun(){
	XY.Clear_Log_Msg();
	XY.Set_Gamge_ForegroundWindow();

	//创建任务
	//TaskList.push(["GoPointMiniMap",GoPointMiniMap,[143,60]])
	// TaskList.push(["GoSwitchMap",GoSwitchMap,["长安城","江南野外"]])
	// TaskList.push(["GoSwitchMap",GoSwitchMap,["江南野外","建邺城"]])
	// TaskList.push(["GoSwitchMap",GoSwitchMap,["建邺城","江南野外"]])
	// TaskList.push(["GoSwitchMap",GoSwitchMap,["江南野外","长安城"]])
	//TaskList.push(["GoSwitchMap",GoSwitchMap,["东海湾","建邺城"]])
	//TaskList.push(["GoSwitchMap",GoSwitchMap,["建邺城","东海湾"]])
	//TaskList.push(["GoSwitchMap",GoSwitchMap,["东海湾","傲来国"]])
	//TaskList.push(["GoSwitchMap",GoSwitchMap,["傲来国","东海湾"]])
	//TaskList.push(["GoSwitchMap",GoSwitchMap,["花果山","傲来国"]])
	//TaskList.push(["GoSwitchMap",GoSwitchMap,["傲来国","花果山"]])
	//TaskList.push(["GoSwitchMap",GoSwitchMap,["北俱芦洲","花果山"]])
	//TaskList.push(["GoSwitchMap",GoSwitchMap,["花果山","北俱芦洲"]])
	// TaskList.push(["GoSwitchMap",GoSwitchMap,["长寿郊外","北俱芦洲"]])
	// TaskList.push(["GoSwitchMap",GoSwitchMap,["北俱芦洲","长寿郊外"]])
	

	//TaskList.push(["GoSwitchMap",GoSwitchMap,["东海湾","建邺城"]])
	//TaskList.push(["GoSwitchMap",GoSwitchMap,["东海湾","傲来国"]])
	//return 
 	TaskList.push(["GoSwitchMap",GoSwitchMap,["长安城","江南野外"]])
 	TaskList.push(["GoSwitchMap",GoSwitchMap,["江南野外","建邺城"]])
 	TaskList.push(["GoSwitchMap",GoSwitchMap,["建邺城","东海湾"]])
 	TaskList.push(["GoSwitchMap",GoSwitchMap,["东海湾","傲来国"]])
 	TaskList.push(["GoSwitchMap",GoSwitchMap,["傲来国","花果山"]])
 	TaskList.push(["GoSwitchMap",GoSwitchMap,["花果山","北俱芦洲"]])
 	TaskList.push(["GoSwitchMap",GoSwitchMap,["北俱芦洲","长寿郊外"]])
 	TaskList.push(["GoSwitchMap",GoSwitchMap,["长寿郊外","长寿村"]])

	TaskList.push(["GoSwitchMap",GoSwitchMap,["长寿村","长寿郊外"]])
	TaskList.push(["GoSwitchMap",GoSwitchMap,["长寿郊外","北俱芦洲"]])
	TaskList.push(["GoSwitchMap",GoSwitchMap,["北俱芦洲","花果山"]])
	TaskList.push(["GoSwitchMap",GoSwitchMap,["花果山","傲来国"]])
	TaskList.push(["GoSwitchMap",GoSwitchMap,["傲来国","东海湾"]])
	TaskList.push(["GoSwitchMap",GoSwitchMap,["东海湾","建邺城"]])
	TaskList.push(["GoSwitchMap",GoSwitchMap,["建邺城","江南野外"]])
	TaskList.push(["GoSwitchMap",GoSwitchMap,["江南野外","长安城"]])

	XY.Add_Log_Msg(XY.MapName);
	

}



///////////////
//
//会一直被调用
//
//////////////
function dorun(){
	TaskState.Run_Times = TaskState.Run_Times + 1 ;
	if(TaskState.Run_Times==1){
		FirstRun();
	}

	XY.Draw_Gamge_Rect(320,240,20,20)

	// var ConfirmRect = XY.Match_Image_Rect("feature/map/to_dohaiwan.png",0.85,1)
	// XY.Draw_Gamge_Rect(ConfirmRect[0],ConfirmRect[1],ConfirmRect[2],ConfirmRect[3])
	// XY.Add_Log_Msg("X:"+ConfirmRect[0]+"  Y:"+ConfirmRect[1])

	if(TaskState.NowRunTaskIndex <= TaskList.length -1){
		var result = TaskList[TaskState.NowRunTaskIndex][1](TaskList[TaskState.NowRunTaskIndex][2],TaskState.CellTaskState);
		if(result){
			TaskState.CellTaskState = [];
			XY.Add_Log_Msg("Task:"+TaskList[TaskState.NowRunTaskIndex][0]+".....OK");
			TaskState.NowRunTaskIndex= TaskState.NowRunTaskIndex+1;
		}
	}else if(TaskState.NowRunTaskIndex == TaskList.length){
		XY.Add_Log_Msg("完成任务");
		TaskState.NowRunTaskIndex= TaskState.NowRunTaskIndex+1;
	}
}
