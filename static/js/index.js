/**
 * Created by 10840 on 2020/3/15.
 */

// 跳转到登录页面
$("#login").on("click", function() {
    window.location.href = login_url;

});

//功能图标跳转
$(".func-item").on("click", function() {
    var viewUrl=$(this).children('p.hide').text()
    window.location.href = "http://127.0.0.1:8000"+viewUrl;
});

//活动详情
$(".activity").on("click", function() {
    var activity_id=$(this).children('p.hide').text()
    window.location.href = activity_d+"?activity_id="+activity_id;
});

//商品详情
$(".pro-item").on("click", function() {
    var pro_id=$(this).children('p.hide').text()
    window.location.href = product_d+"?pro_id="+pro_id;
});

//更多活动
$("#activity_more").on("click", function () {
    window.location.href = activity_more+"?page=1";
})

//更多商品
$("#pro_more").on("click", function () {
    window.location.href = product;
})

//去社区
$("#community").on('click', function () {
    window.location.href = enter_community;
})