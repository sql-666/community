/**
 * Created by 10840 on 2020/4/25.
 */

$(function () {
    var now_tpye = $(".type-head").attr("now_type")
    if (now_tpye=="all"){
        $("label.wrap-type-name").children("input[value='all']").attr("checked","true")

    }else if(now_tpye=="meets"){
        $("label.wrap-type-name").children("input[value='meets']").attr("checked","true")

    }else if(now_tpye=="vegetables"){
        $("label.wrap-type-name").children("input[value='vegetables']").attr("checked","true")

    }else if(now_tpye=="manual"){
        $("label.wrap-type-name").children("input[value='smoke']").attr("checked","true")

    }else if(now_tpye == "fruits"){
        $("label.wrap-type-name").children("input[value='fruits']").attr("checked","true")
    }

})

$("label.wrap-type-name").on('click', function () {
    var type = $(this).children("input.radio").val()
    window.location.href = product+"?type="+type+"&page_id=1";
})

//商品详情
$(".pro").on("click", function() {
    var pro_id=$(this).children('img.proImg').attr("value")
    window.location.href = product_d+"?pro_id="+pro_id;
});

//搜索
$("#search").on('blur',function(){
    alert("xxxx")
})