setScreenMetrics(1080,2340)
var api_host = "http://192.168.21.71:21000/"
var old_clip = ''
// 按钮位置
// 搜索按钮位置
var search_button_x = 1000
var search_button_y = 148
// 搜索-视频
var ser_video_x= 294
var ser_video_y = 264
// 搜索-视频-第一个
var video_1_x = 224
var video_1_y = 739

// 输入法
// 字母位置
var x_x = 344
var x_y = 1936
var j_x = 725
var j_y = 1765

// 输入法第一个
var input_1_x = 120
var input_1_y = 1475

// 复制链接比对模板
var img_64 = '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'
img = images.fromBase64(img_64)
// img = images.read('./douyin.png');
small = images.detectAndComputeFeatures(img)
img.recycle()

// 打开抖音
launchApp("抖音");
sleep(5000);
// 截图权限
images.requestScreenCapture();
sleep(3000);
// text('立即开始').depth(2).click();
sleep(1000);
// 搜索小姐姐
function search_sister(){
    // 点击搜索
    click(search_button_x,search_button_y);
    sleep(2000);
    click(x_x,x_y);
    click(j_x,j_y);
    click(j_x,j_y);
    click(input_1_x,input_1_y);
    click(search_button_x,search_button_y);
    sleep(2000);
    // 选择视频
    click(ser_video_x,ser_video_y);
    sleep(3000);
    click(video_1_x,video_1_y);
}
// 人脸数据
function face_info(){
    try {
        i = images.captureScreen();
        i_64 = images.toBase64(i, "jpeg", 50);
        i.recycle();
        var url = api_host+"face";
        r = http.postJson(url, {
            url: "",
            image: i_64,
        });
        if (r.body.json()['code'] != 200){
            return {'Beauty':0,'Age':88};
        }
        return JSON.parse(r.body.json()['data'])['FaceAttributesInfo']
    } catch (error) {
        console.log(error)
        return {'Beauty':0,'Age':99}
    }

}
// 下滑视频
function next(){
    start_x = 493+random(-300,300);
    start_y = 1066+random(-100,200);
    swipe(start_x, start_y, start_x+random(-50,50), start_y-random(500,800), random(100,300));
}
// 点赞
function love(){
    click(998+random(-5,5),1323+random(-5,5));
}
// 复制链接
function copy(){
    click(998+random(-5,5),1891+random(-5,5));
    sleep(2000);
    start_x = 886+random(-10,10);
    start_y = 2154+random(-10,10);
    swipe(start_x, start_y, start_x+random(-600,-450), start_y-random(-50,100), random(100,300));
    sleep(2000)
    i = images.captureScreen();
    clip = images.clip(i, 0, 1691, 1080, 649);
    big = images.detectAndComputeFeatures(clip);
    res = images.matchFeatures(scene=big,object=small);
    click(res.centerX+random(-10,10),res.centerY+1691+random(-10,10));
    big.recycle()
    clip.recycle()
    i.recycle()
}

// 视频链接解析
function video_url(video_link){
    try {
        var url = api_host+"video_link_analysis";
        r = http.postJson(url, {
            video_link:video_link,
        });
        if (r.body.json()['code'] != 200){
            return {'author':'0','title':'0','cover':'0','url':'0'}
        }
        return r.body.json()['data']
    } catch (error) {
        console.log(error)
        return {'author':'0','title':'0','cover':'0','url':'0'}
    }
}

// 下载文件
function download(uuid,f_name,f_url,path){
    try {
        var url = api_host+"download_to_server";
        r = http.postJson(url, {
            uuid:uuid,
            file_name:f_name,
            url:f_url,
            save_path:path
        });
    } catch (error) {
        console.log(error)
    }
}

// 获取uuid
function get_uuid(text){
    try {
        var url = api_host+"uuid";
        r = http.postJson(url, {
            text:text
        });
        if (r.statusCode != 200){
            get_uuid(text)
        }
        return r.body.string()
    } catch (error) {
        console.log(error)
    }
}

// 素材信息入数据库
function insert_mysql(uuid,title){
    try {
        var url = api_host+"insert_mysql";
        r = http.postJson(url, {
            table:"source_info(uuid,title,data_type,inner_type,style,origin_time)",
            data:"('"+[uuid,title,'抖音','小姐姐','小姐姐',now_datetime()].join("','")+"')",
            condition:''
        });
    } catch (error) {
        console.log(error)
    }
}
// 当前日期格式化为yyyy-MM-dd  hh:mm:ss
function now_datetime()
	{
		//dataString是整数，否则要parseInt转换
        var dataString = Date.parse(new Date())
		var time = new Date(dataString);
		var year = time.getFullYear();
		var month = time.getMonth()+1;
		var day = time.getDate();
		var hour = time.getHours();
		var minute = time.getMinutes();
		var second = time.getSeconds();
		return year+'-'+(month<10?'0'+month:month)+'-'+(day<10?'0'+day:day)+' '+(hour<10?'0'+hour:hour)+':'+(minute<10?'0'+minute:minute)+':'+(second<10?'0'+second:second)
	}

// 观看视频
function watch(){
    try {
        launchApp('抖音')
        sleep(1000+random(1000,3000))
        info = face_info();
        toast('年龄：'+ info['Age']+' 人脸评分：' + info['Beauty'])
        if (info['Beauty']>90 && info['Age']<30){
            love();
            sleep(1000);
            copy();
            sleep(1000);
            launchApp("AutoJsPro");
            sleep(1000);
            var clips = getClip()
            if(clips == old_clip){
                back()
                sleep(3000)
                back()
                sleep(3000)
                launchApp('抖音')
                sleep(2000)
            }
            else{
                old_clip = clips
                console.log(clips)
                detail = video_url(clips)
                title = detail['author']+'_'+detail['title']
                if (title == '0_0' || title == 'null_null'){
                    return 0;
                }
                uuid = get_uuid('抖音'+'小姐姐'+title)
                insert_mysql(uuid,title)
                cover = detail['cover']
                video = detail['url']
                launchApp("抖音");
                sleep(1000)
                download(uuid,title+'.mp4',video,'/mnt/l1/short_video/douyin/sister/video/')
                download(uuid,title+'.jpg',cover,'/mnt/l1/short_video/douyin/sister/cover/')
            }
            next();
        }
        else next();
    } catch (error) {
        console.error(error)
        back()
        sleep(3500)
        back()
        sleep(3500)
        back()
        sleep(3500)
        launchApp('抖音')
        sleep(5000)
        next()
    }
}
function run(){
    for (x=0;x<50000;x++){
        watch()
    }
    small.recycle()
    return 0
};
run()