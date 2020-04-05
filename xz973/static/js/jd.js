$(document).ready(function(){
    var pg = document.getElementById("pg");
    var jdstar = setInterval(function(){
        if(pg.value!=100) {
            $.ajax({url:"jd",success:function(data){pg.value=data.jd}});
        }else{
            clearInterval(jdstar);
            alert("采集完毕");
        };
    },500);
});
