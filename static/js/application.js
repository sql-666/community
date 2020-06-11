/**
 * Created by 10840 on 2020/4/25.
 */

$("#submit").on('click', function () {
    var data={
        spe : $('#spe').val(),
        reason : $('#reason').val()
    }
    if (!(empty(spe) & empty(reason)) ){
         $.ajax({
        type: 'POST',
        url: application,
        data: JSON.stringify(data),
        dataType:"json",
        contentType:"application/json;charset=utf-8",
        success: function (res) {
            if (res.code=="200") {//根据返回值进行跳转
                window.location.href = volunteers+"?page_id=1";
            }else{
                alert("服务繁忙，请稍后提交！")
            }
        }
    });
    }
})

