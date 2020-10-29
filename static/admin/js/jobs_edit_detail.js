function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function(){
    $(".jobs_edit").submit(function (e) {
        // 阻止表单默认提交行为
        e.preventDefault();

        // 获取news_id
        var jobs_id = $(".jobs_edit").attr("data-jobs-id");

        // TODO 新闻编辑提交
        $(this).ajaxSubmit({
            //  beforeSubmit: function (request) {
            //     // 在提交之前，对参数进行处理
            //     for(var i=0; i<request.length; i++) {
            //         var item = request[i];
            //         if (item["name"] == "content") {
            //             item["value"] = tinyMCE.activeEditor.getContent()
            //         }
            //     }
            // },
            url: "/admin/jobs_edit_detail/" + jobs_id,
            type: "POST",
            headers: {
                "X-CSRFToken": getCookie('csrf_token')
            },
            success: function (resp) {

                if (resp.errno == "0") {
                    // `编辑新闻`成功
                    // alert('编辑成功');
                    window.location.href="/admin/jobs_edit.html"
                }
                else {
                    // `编辑新闻`失败
                    alert(resp.errmsg);
                    window.location.href="/admin/jobs_edit.html"
                }
            }
        });
    })
});

// 点击取消，返回上一页
function cancel() {
    history.go(-1);
}