$(document).ready(function() {
    // 登出按钮
    $("#logout-button").bind("click", function() {
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/api/user/logout/",
            cache: false,
            success: function (data) {
                window.location.href = data["redirect_url"];
            }
        });
    });
});