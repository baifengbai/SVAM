setScreenMetrics(1080,2340)
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
img = images.read('/sdcard/douyin.png');
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
        var url = "http://192.168.21.71:21000/face";
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
}

// 视频链接解析
function video_url(video_link){
    try {
        var url = "http://192.168.21.71:21000/video_link_analysis";
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
function download(f_name,f_url,path){
    try {
        var url = "http://192.168.21.71:21000/download_to_server";
        r = http.postJson(url, {
            file_name:f_name,
            url:f_url,
            save_path:path
        });
    } catch (error) {
        console.log(error)
    }
}

// 观看视频
function watch(){
    try {
        sleep(1000+random(1000,3000))
        info = face_info();
        console.log(info['Beauty'])
        if (info['Beauty']>90 && info['Age']<30){
            love();
            sleep(2000);
            copy();
            sleep(1000);
            // start_x = 428
            // start_y = 2339
            // swipe(start_x, start_y, start_x+random(-50,50), start_y+random(-800,-600), random(700,800));
            // sleep(1000)
            // click(826,1344)
            // sleep(2000)
            launchApp("AutoJsPro");
            sleep(1000);
            var clips = getClip()
            if(clips == old_clip){
                back()
                sleep(1000)
                back()
                sleep(1000)
            }
            else{
                console.log(clips)
                detail = video_url(clips)
                author = detail['author']
                title = detail['title']
                cover = detail['cover']
                video = detail['url']
                launchApp("抖音");
                sleep(1000)
                download(author+'_'+title+'.mp4',video,'/mnt/l1/short_video/douyin/sister/video/')
                download(author+'_'+title+'.jpg',cover,'/mnt/l1/short_video/douyin/sister/cover/')
            }
            next();
        }
        else next();
    } catch (error) {
        next()
    }
}
for (x=0;x<50000;x++){
    watch()
}
small.recycle()