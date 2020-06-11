/**
 * Created by 10840 on 2020/4/23.
 */
$(".item").on('click',function () {
    var url=$(this).children("p.hide").text()
    window.location.href = "http://127.0.0.1:8000"+url
})
