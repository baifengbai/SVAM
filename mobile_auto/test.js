var api_host = "http://192.168.21.71:21000/"
function get_uuid(text){
    try {
        var url = api_host+"uuid";
        r = http.postJson(url, {
            text:text
        });
        return r.body.string()
    } catch (error) {
        console.log(error)
    }
}

function timestampToTime() {
    let date = new Date()
    year = date.getYear()
    month = date.getMonth()
    day = date.getDay()
    hour = date.getHours()
    minute = date.getMinutes()
    second = date.getSeconds()
    return year + '-' + month + '-' + day + ' ' + hour + ':' +minute + ':' + second
}

function format()
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

// "2021-05-08 12:50:30"


let date = new Date()
console.log(format())