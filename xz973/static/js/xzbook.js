$(document).ready(function(){
    $("#btn").on("click",function(){
        $.get("ceshi",{name:$("#namevalue").val()},function(data){
            var list1 =data
            var ulobj = document.createElement("ul");
            var div1 = document.getElementById("div1");
            div1.appendChild(ulobj);
            for(var i = 0 ; i < list1.length ; i++){
                
                var liobj = document.createElement("li");
                var nameobj = document.createElement("span");
                var zzobj = document.createElement("span");
                var newobj = document.createElement("span");
                nameobj.name=list1[i].url;
                nameobj.id=("s1");
                zzobj.id=("s2");
                newobj.id=("s3");
                nameobj.innerHTML=list1[i].name;
                zzobj.innerHTML=list1[i].zz;
                newobj.innerHTML=list1[i].new;
                liobj.appendChild(nameobj,zzobj,newobj);
                liobj.appendChild(zzobj);
                liobj.appendChild(newobj);
                ulobj.appendChild(liobj);

                nameobj.onmouseover = spanjd;
                nameobj.onmouseout = spanlk;
                nameobj.onclick = clickspan;
            }
        })
    }); 
});
//鼠标进入离开事件
function spanjd(){
    this.style.backgroundColor = "red";
};
function spanlk(){
    this.style.backgroundColor = "";
};
function clickspan(){
    alert("采集的书名是"+this.innerHTML);
    $.get("xzdata", {name:this.innerHTML,url:this.name});
    window.location.replace("/jdye");
}