images.requestScreenCapture()
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
console.log(face_info())
