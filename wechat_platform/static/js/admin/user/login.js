define(function(require, exports, module) {
    require('common');
    require('jquery-validate');
    var $ = require('jquery');

    $("#login-form").validate({
        rules: {
            username: "required",
            password: "required"
        },
        messages: {
            username: {
                required: "用户名不能为空"
            },
            password: {
                required: "密码不能为空"
            }
        },
        highlight: function(element) {
            $(element).parent().addClass("has-error");
        },
        unhighlight: function(element) {
            $(element).parent().removeClass("has-error");
        },
        submitHandler: function(form) {
            var validator = this;

            $.ajax({
                type: "POST",
                dataType: "json",
                url: "/api/user/login/",
                cache: false,
                data: {
                    username: $("input[name=username]").val(),
                    password: $("input[name=password]").val(),
                    next: $("input[name=next]").val()
                },
                beforeSend: function() {
                    $("button[type=submit]").attr("disabled", "disabled");
                    $("button[type=submit]").text("登录中…");
                },
                success: function(data) {
                    window.location.href = data["redirect_url"];
                },
                statusCode: {
                    400: function(xhr) {
                        var data = $.parseJSON(xhr.responseText);
                        var errors = {};
                        for (var key in data) {
                            if (key == "non_field_errors") {
                                errors["password"] = data[key][0];
                            } else {
                                errors[key] = data[key][0];
                            }
                        }
                        validator.showErrors(errors);
                    }
                },
                complete: function() {
                    $("button[type=submit]").removeAttr("disabled");
                    $("button[type=submit]").text("登录");
                }
            });
            return false;
        }
    });
});
