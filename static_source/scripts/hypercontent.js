(function () {
    var getParams = parseGetParamsMVT();
    var site = window.location.hostname;
    var mvtid = getParams['mvtid'];
    var mvt_cookie_id = '';
    if (!mvtid) {
        var mvt_cookie_id = get_cookie_mvt('MVT_ID');
        if (mvt_cookie_id) {
            mvtid = mvt_cookie_id;
        }
    }
    if (mvtid) {
        var mvt_interval = 1000 * 3600 * 24 * 7; //секунда * час * сутки * неделя, время действия куки
        var mvt_date = new Date ( ); // Текущая дата и время
        var mvt_date_now = new Date ( ); // Текущая дата и время
        mvt_date.setTime ( mvt_date.getTime() + mvt_interval );

        //если новый параметр в гет И он не равен старому
        if((mvt_cookie_id == '') && (mvtid != get_cookie_mvt('MVT_ID'))) {
            document.cookie = "MVT_ID=" + mvtid + "; expires=" + mvt_date.toGMTString();
            document.cookie = "MVT_ID_TIME=" + mvt_date_now.getTime() + "; expires=" + mvt_date.toGMTString();
            var mvt_xhr = new XMLHttpRequest();
            mvt_xhr.open("GET", 'http://adfor.ru/mvtsendset/' + site + '/' + mvtid + '/' + '4', true);
            mvt_xhr.send();
        }
        document.getElementsByTagName('body')[0].setAttribute("style", "opacity:0;");
        var s = document.createElement('script');
        s.type = 'text/javascript';
        s.async = true;
        s.src = '//adfor.ru/mvtscript/' + site + '/' + mvtid + '/' + '4';
        var ss = document.getElementsByTagName('script')[0];
        ss.parentNode.insertBefore(s, ss);
        var mvt_cookie_time = get_cookie_mvt('MVT_ID_TIME');
        var time_interval = mvt_date_now.getTime() - mvt_cookie_time;
        var mvt_interval_send = 1000 * 3600;

        //интервал отправки сообщения о повторном заходе по набору
        if(time_interval > mvt_interval_send) {
            document.cookie = "MVT_ID_TIME=" + mvt_date_now.getTime() + "; expires=" + mvt_date.toGMTString();
            var mvt_xhr = new XMLHttpRequest();
            mvt_xhr.open("GET", 'http://adfor.ru/mvtsendsetrepeat/' + site + '/' + mvtid + '/' + '4', true);
            mvt_xhr.send();
        }
    }
})();

function parseGetParamsMVT() {
    var $_GET = {};
    var __GET = window.location.search.substring(1).split("&");
    for(var i=0; i<__GET.length; i++) {
        var getVar = __GET[i].split("=");
        $_GET[getVar[0]] = typeof(getVar[1])=="undefined" ? "" : getVar[1];
    }
    return $_GET;
}

function get_cookie_mvt(cookie_name) {
    var results = document.cookie.match ('(^|;) ?' + cookie_name + '=([^;]*)(;|$)');
    if ( results )
        return ( unescape ( results[2] ) );
    else
        return null;
}