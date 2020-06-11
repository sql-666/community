/**
 * Created by 10840 on 2020/4/28.
 */
$(".btn").on('click', function () {
    data = [{
        value: $("#title").val(),
        len: 20,
        bt: "title",
        x_bt: "标题"
    }, {
        value: $("#price").val(),
        len: 10,
        bt: "price",
        x_bt: "价格"
    }, {
        value: $("#unit").val(),
        len: 3,
        bt: "unit",
        x_bt: "单位"
    },{
        value:$("#inventory").val(),
        len: 5,
        bt: "inventory",
        x_bt: "库存"
    }, {
        value: $("#start_price").val(),
        len: 10,
        bt: "start_price",
        x_bt: "起卖价"
    }, {
        value: $("#type").val(),
        len: 10,
        bt: "type",
        x_bt: "类型"
    }, {
        value: $("#phone").val(),
        len: 11,
        bt: "phone",
        x_bt: "联系电话"
    }, {
        value: $("#get_type").val(),
        len: 20,
        bt: "get_type",
        x_bt: "拿货方式"
    }, {
        value: $("#note").val(),
        len: 50,
        bt: "note",
        x_bt: "备注"
    }]

    for (var i = 0; i < data.length; i++) {
        if (data[i]["bt"] != "note") {
            if (empty(data[i]["value"])) {

                $("#warning").css('display', 'block')
                $("#warning").children("span").text(data[i]["x_bt"] + "格式错误！")
                return
            }
        }

    }
    var type=$(".wrap").attr("mytype")
    if (type=="edit"){
        var pro_id = $(".wrap").attr("pro_id")
        myurl="?type="+type+"&pro_id="+pro_id
    }else{
        myurl="?type="+type
    }

    $.ajax({
        type: 'POST',
        url: edit_product+myurl,
        data: JSON.stringify(data),
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        success: function (res) {
            if (res.code == "200") {//根据返回值进行跳转
                alert("添加成功")
                window.location.href = my_product;
            } else{
                $("#warning").children("span").text("添加失败！")
                $("#warning").show()
            }
        }
    })

})
