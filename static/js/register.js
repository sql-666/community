/**
 * Created by 10840 on 2020/4/24.
 */

//发送验证码
$("#basic-addon2").on('click', function () {
    var account = $('#username').val()
    if (account.length !=11){
        $("#warning").children("span").text("请输入正确格式的账号！")
        $("#warning").show()
        return
    }
    var data={
        "account":account
    }
    $.ajax({
        type: 'POST',
        url: phone_code,
        data:JSON.stringify(data),
        success: function (res) {
            if (res.code=="200") {//根据返回值进行跳转
                alert("发送成功！请查收")
            }
        }
    });
})



$("#register").on('click', function () {
    var text=""
    if (empty($('#username').val())){
        text="账号不能为空！"
        $("#warning").children("span").text(text)
        $("#warning").show()
        return
    }else if(empty($('#password').val())){
        $("#warning").children("span").text("密码不能为空！")
        $("#warning").show()
        return
    }else if(empty($('#password_again').val())){
        $("#warning").children("span").text("确认密码不能为空！")
        $("#warning").show()
        return
    }else if ($('#password').val() != $('#password_again').val()){
        $("#warning").children("span").text("两次密码不一致！")
        $("#warning").show()
        return
    } else if(empty($('#captcha').val())) {
        $("#warning").children("span").text("验证码不能为空！")
        $("#warning").show()
        return
    }
    var data={
        username:$('#username').val(),
        password:$('#password').val(),
        password_again:$('#password_again').val(),
        captcha:$('#captcha').val()
    }
    console.log(data)
    $.ajax({
        type: 'POST',
        url: register,
        data:JSON.stringify(data),
        dataType:"json",
        contentType:"application/json;charset=utf-8",
        success: function (res) {
            if (res.code=="200") {//根据返回值进行跳转
                window.location.href = 'http://127.0.0.1:8000/myapp/login';
            }
        }
    });
})
