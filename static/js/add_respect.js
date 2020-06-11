/**
 * Created by 10840 on 2020/4/24.
 */

$(".btn").on('click', function () {
    var data={
        name:$("#name").val(),
        avatar:$("#avatar").val(),
        age:$("#age").val(),
        gender:$("input[name='gender']:checked").val(),
        single:$("input[name='widowed']:checked").val(),
        note:$("#note").val(),
        live_situation:$("#live_situation").val(),
        health_situation:$("#health_situation").val(),
        address:$("#address").val(),
        hobby:$("#hobby").val(),
        phone:$("#phone").val(),
        families:$("#families").val()

    }
    $.ajax({
        type: 'POST',
        url: add_respect,
        data: JSON.stringify(data),
        dataType:"json",
        contentType:"application/json;charset=utf-8",
        success: function (res) {
            if (res.code=="200") {//根据返回值进行跳转
                window.location.href = help_respects+"?page_id=1";
            }else{
                $("#warning").children("span").text("格式错误")
                $("#warning").show()
            }
        }
    });
})

