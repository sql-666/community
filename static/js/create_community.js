/**
 * Created by 10840 on 2020/4/27.
 */

$('#create-btn').on('click', function () {
    var data = [{
        value: $("#community_name").val(),
        len: 10,
        bt:"community_name",
        x_bt:"社区名"
    },{
        value:$("#province").val(),
        len:10,
        bt:"province",
        x_bt:"省市"
    }, {
        value:$("#address").val(),
        len:10,
        bt:"address",
        x_bt:"地址"
    },{
        value: $("#account").val(),
        len: 11,
        bt: "account",
        x_bt:"账号"
    },{
        value: $("#code").val(),
        len: 4,
        bt: "code",
        x_bt:"验证码"
    }]

    for (var i = 0; i < data.length; i++) {
        if (empty(data[i]["value"]) || !string_len(data[i]["value"], data[i]["len"])) {
            $("#warning").css('display', 'block')
            $("#warning").children("span").text(data[i]["x_bt"] + "格式错误！")
            return
        }
    }
     $.ajax({
        type: 'POST',
        url: create_community,
        data: JSON.stringify(data),
        dataType:"json",
        contentType:"application/json;charset=utf-8",
        success: function (res) {
            if (res.code=="200") {//根据返回值进行跳转
                window.location.href = mycommunity;
            }else if(res.code=="600"){
                $("#warning").children("span").text("重复操作！")
                $("#warning").show()

            }else if(res.code=="401"){
                $("#warning").children("span").text("请使用当前登录账号！")
                $("#warning").show()
            }else{
                $("#warning").children("span").text("格式错误！")
                $("#warning").show()
            }
        }
    });


})