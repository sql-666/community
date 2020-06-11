/**
 * Created by 10840 on 2020/4/23.
 */
$(function () {
    var now_gender = $("#gender").attr("now_gender")
    if (now_gender=="1"){
        $("label").children("input[value='1']").attr("checked","true")
    }else{
        $("label").children("input[value='2']").attr("checked","true")
    }

})


$("#edit-user-info-btn").on("click", function () {
    var data={
        name: $("#name").val(),
        occupation:$("#occupation").val(),
        specialty:$("#specialty").val(),
        content:$("#content_note").val(),
        gender:$("label").children("input[checked='checked']").val(),
        age:$("#age").val()
    }
    $.ajax({
        type: 'POST',
        url: edit_user_info,
        data: JSON.stringify(data),
        dataType:"json",
        contentType:"application/json;charset=utf-8",
        success: function (res) {
            console.log(res);
            if (res.code=="200"){
                alert("修改成功");
            }else{
                alert("修改失败");
            }

        }

    });


})
