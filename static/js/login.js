/**
 * Created by 10840 on 2020/4/7.
 */
$("#login-btn").on("click", function() {
    var data={
        username:$('#username').val(),
        password:$('#password').val(),
        rememberMe:$('#rememberMe').val()
    }
    $.ajax({
        type: 'POST',
        url: login,
        data: JSON.stringify(data),
        dataType:"json",
        contentType:"application/json;charset=utf-8",
        success: function (res) {
            if (res.code=="200") {//根据返回值进行跳转
                window.location.href = index;
            }else{
                $("#warning").children("span").text("账号或密码错误")
                $("#warning").show()
            }
        }
    });
});

$("a").on('click', function () {
    window.location.href = register;
})











