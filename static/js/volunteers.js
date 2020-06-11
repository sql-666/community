/**
 * Created by 10840 on 2020/4/23.
 */
//onready
$(function() {
    var now_type = $("#nav").children("p.hide").text()
    var page_id = $(".nav-page").attr("page_id")
    // $("li[click_type=now_type]").addClass("active")
    if (now_type == "all") {
        $("li[click_type='all']").addClass("active")
    } else if (now_type == "active") {
        $("li[click_type='active']").addClass("active")
    } else if (now_type == "deadline") {
        $("li[click_type='deadline']").addClass("active")
    } else if (now_type == "end") {
        $("li[click_type='end']").addClass("active")
    }

    // if (page_id == "1") {
    //     $("li[name='first']").children("a").addClass("page-active")
    // }
});


$("li[name='pre']").on('click', function () {
    var now_id = $(".nav-page").attr("page_id")
    if (int(now_id) ==1){
        alert("当前为首页！")
        return
    }
    var page_id = int(now_id)-1
     window.location.href = volunteers+"?type="+click_type+"&page_id="+page_id.toString();
})

$("li[name='next']").on('click', function () {
    var now_id = $(".nav-page").attr("page_id")
    var page_id = int(now_id)+1
     window.location.href = volunteers+"?type="+click_type+"&page_id="+page_id.toString();
})

$("li[name='end']").on('click', function () {
     window.location.href = volunteers+"?type="+click_type+"&page_id=0";
})



$(".activity-item").on('click',function () {
    var activity_id = $(this).children("p.hide").text()
    window.location.href =activity_d+"?activity_id="+activity_id
})

$("li[role='presentation']").on("click", function () {
    var click_type=$(this).attr("click_type")

    $("li[role='presentation']").removeClass("active")
    // $(this).addClass("active")
    // alert($(this).text())
    window.location.href = volunteers+"?type="+click_type+"&page_id=1";
})

$("button").on('click', function () {
    window.location.href = application

})

