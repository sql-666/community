/**
 * Created by 10840 on 2020/4/22.
 */
//跳转到详情页面
$(".respect-item").on('click', function () {
    var respect_id = $(this).children('p.hide').text()
    window.location.href=respects_detail+"?respect_id="+respect_id
})

$(".wrap-btn").on('click', function () {
     window.location.href=add_respect
})
