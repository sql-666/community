/**
 * Created by 10840 on 2020/4/28.
 */
$("#add-img").on('click',function () {
     window.location.href = edit_product+"?type=new";
})

$(".del").on('click', function () {
    var pro_id = $(this).attr("pro_id")
    $.ajax({
        type: 'GET',
        url: edit_product+"?type=del&pro_id="+pro_id,
        dataType:"json",
        contentType:"application/json;charset=utf-8",
        success: function (res) {
            if (res.code=="200") {//根据返回值进行跳转
                window.location.href = my_product;
            }
        }
    });
})

$(".content").on('click',function () {
    var pro_id = $(this).attr("pro_id")
    window.location.href = edit_product+"?type=edit&pro_id="+pro_id;
})