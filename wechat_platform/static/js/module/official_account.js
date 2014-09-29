define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var ConfirmModal = require('helper.confirm-modal');
    require('jquery-validate');
    require('jquery-cookie');

    var item_template = require('text!templates/official_account/item.html');
    var list_template = require('text!templates/official_account/list.html');
    var detail_template = require('text!templates/official_account/detail.html');
    var add_template = require('text!templates/official_account/edit.html');
    var edit_template = require('text!templates/official_account/edit.html');

    var confirm_modal_view = new ConfirmModal;

    var OfficialAccount = Backbone.Model.extend({
        urlRoot: '/api/official_account/'
    });
    var OfficialAccounts = Backbone.Collection.extend({
        url: '/api/official_account/',
        model: OfficialAccount
    });

    var OfficialAccountItemView = Backbone.View.extend({
        template: _.template(item_template),
        initialize: function(args) {
            this.model = args.model;
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destroy', this.remove);
        },
        events: {
            "click .delete": "delete_item"
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        delete_item: function() {
            var current_model = this.model;
            confirm_modal_view.show({
                cb: function() {
                    current_model.destroy({
                        wait: true,
                        success: function(model, response) {
                            noty({
                                type: "success",
                                text: "成功删除 <strong>" + model.get('name') + "</strong> 公众号"
                            });
                        },
                        error: function(model, response) {
                            noty({
                                type: "error",
                                text: "尝试删除 <strong>" + model.get('name') + "</strong> 公众号时出错，请重试"
                            });
                        }
                    });
                },
                title: "确认删除",
                body: "请确认您将删除 <strong><u>" + this.model.get('name') + "</u></strong> 公众号，该操作不可恢复。"
            });
        }
    });

    var OfficialAccountItemDetailView = Backbone.View.extend({
        template: _.template(detail_template),
        initialize: function(args) {
            this.official_account = new OfficialAccount({id: args.id});
            this.listenTo(this.official_account, 'change', this.render_official_account)
        },
        events: {
            'click .delete': 'delete_item'
        },
        render: function() {
            this.$el.html(this.template({id: this.official_account.id}));
            this.render_official_account(this.official_account);
            this.official_account.fetch();
            return this;
        },
        render_official_account: function(official_account) {
            this.$('#account-name').html(official_account.get('name'));
            this.$('#account-request-url').html(official_account.get('request_url'));
            this.$('#account-token').html(official_account.get('token'));
            this.$('#account-level').html(official_account.get('level_readable'));
            if (official_account.get('is_advanced')) {
                this.$('#account-is-advanced').html('是');
            } else {
                this.$('#account-is-advanced').html('否');
            }

            this.$('#account-appid').html(this.transform_value(official_account.get('appid')));
            this.$('#account-appsecret').html(this.transform_value(official_account.get('appsecret')));
            this.$('#account-username').html(this.transform_value(official_account.get('username')));
            this.$('#account-password').html(this.transform_value(official_account.get('password')));
            this.$('#account-email').html(this.transform_value(official_account.get('email')));
            this.$('#account-original').html(this.transform_value(official_account.get('original')));
            this.$('#account-wechat').html(this.transform_value(official_account.get('wechat')));
            this.$('#account-introduction').html(this.transform_value(official_account.get('introduction')));
            this.$('#account-address').html(this.transform_value(official_account.get('address')));
        },
        delete_item: function() {
            var current_model = this.official_account;
            confirm_modal_view.show({
                cb: function() {
                    current_model.destroy({
                        wait: true,
                        success: function(model, response) {
                            noty({
                                type: "success",
                                text: "成功删除 <strong>" + model.get('name') + "</strong> 公众号"
                            });
                            window.location.href = '#';
                        },
                        error: function(model, response) {
                            noty({
                                type: "error",
                                text: "尝试删除 <strong>" + model.get('name') + "</strong> 公众号时出错，请重试"
                            });
                        }
                    });
                },
                title: "确认删除",
                body: "请确认您将删除 <strong><u>" + this.official_account.get('name') + "</u></strong> 公众号，该操作不可恢复。"
            });
        },
        transform_value: function(value) {
            if (value === null) {
                return '尚未填写'
            } else {
                return value;
            }
        }
    });

    var OfficialAccountListView = Backbone.View.extend({
        template: _.template(list_template),
        initialize: function() {
            this.collection = new OfficialAccounts;
            this.listenTo(this.collection, 'add', this.add);
        },
        render: function() {
            var that = this;
            this.$el.html(this.template());
            _(this.collection.models).each(this.add, this);
            this.collection.fetch({
                success: function(collection) {
                    if (!collection.length) {
                        that.$('#no-official-account').css('display', 'block');
                    }
                }
            });
            return this;
        },
        add: function(official_account) {
            var official_account_view = new OfficialAccountItemView({model: official_account});
            this.$('#no-official-account').css('display', 'none');
            this.$(".list").append(official_account_view.render().el);
        }
    });

    var OfficialAccountItemAddView = Backbone.View.extend({
        template: _.template(add_template),
        initialize: function() {},
        /**
         * 渲染添加公众号页面
         * @returns {OfficialAccountItemAddView}
         */
        render: function() {
            this.$el.html(this.template());
            this.set_validate();
            this.$('input[name=level]').on('change', this, this.toggle_level);
            this.$('input[name=is_advanced]').on('change', this, this.toggle_is_advanced);
            return this;
        },
        /**
         * 获得当前用户选择的公众号级别
         * @returns {string}
         */
        get_level: function() {
            return this.$el.find('input[name=level]:checked').val();
        },
        /**
         * 判断当前用户是否选择了开启高级支持
         * @returns {boolean}
         */
        get_is_advanced: function() {
            // jQuery-Validation 对 undefined 情况处理不好
            if (this.$el.find('input[name=is_advanced]:checked').val() === '1') {
                return true;
            } else {
                return false;
            }
        },
        /**
         * 切换公众号等级下面的AppID和AppSecret的显示和隐藏
         * @param event
         */
        toggle_level: function(event) {
            if (event.data.$el.find('input[name=level]:checked').val() === '1') {
                event.data.$('#level_div').css('display', 'none');
            } else {
                event.data.$('#level_div').css('display', 'block');
            }
        },
        /**
         * 切换高级支持下面的公众平台用户名和密码的显示和隐藏
         * @param event
         */
        toggle_is_advanced: function(event) {
            if (event.data.$el.find('input[name=is_advanced]:checked').val() === '1') {
                event.data.$('#is_advanced_div').css('display', 'block');
            } else {
                event.data.$('#is_advanced_div').css('display', 'none');
            }
        },
        /**
         * 设置表单的验证
         */
        set_validate: function() {
            var that = this;
            this.$el.find('#form').validate({
                rules: {
                    name: 'required',
                    level: 'required',
                    appid: {
                        required: function(element) {
                            return that.get_level() == 2 || that.get_level() == 3;
                        }
                    },
                    appsecret: {
                        required: function(element) {
                            return that.get_level() == 2 || that.get_level() == 3;
                        }
                    },
                    is_advanced: 'required',
                    username: {
                        required: function(element) {
                            return that.get_is_advanced();
                        }
                    },
                    password: {
                        required: function(element) {
                            return that.get_is_advanced();
                        }
                    },
                    email: {
                        required: true,
                        email: true
                    },
                    original: 'required',
                    wechat: 'required'
                },
                messages: {
                    name: {
                        required: '公众号名称不能为空'
                    },
                    level: {
                        required: '必须选择一个公众号级别'
                    },
                    appid: {
                        required: '当前公众号级别必须填入App ID'
                    },
                    appsecret: {
                        required: '当前公众号级别必须填入App Secret'
                    },
                    is_advanced: {
                        required: '必选选择是否开启高级支持'
                    },
                    username: {
                        required: '开启高级支持时必须输入公众平台用户名'
                    },
                    password: {
                        required: '开启高级支持时必须输入公众平台密码'
                    },
                    email: {
                        required: '登录邮箱不能为空',
                        email: '登录邮箱不合法'
                    },
                    original: {
                        required: '原始ID不能为空'
                    },
                    wechat: {
                        required: '绑定微信号不能为空'
                    }
                },
                errorClass: 'control-label text-red',
                errorPlacement: function(error, element) {
                    if ($(element).prop('name') == 'level' || $(element).prop('name') == 'is_advanced') {
                        $(element).parent().parent().append(error);
                    } else {
                        error.insertAfter(element);
                    }
                },
                highlight: function(element) {},
                unhighlight: function(element) {},
                submitHandler: function(form) {
                    var validator = this;

                    $.ajax({
                        type: 'POST',
                        dataType: 'json',
                        url: '/api/official_account/',
                        cache: false,
                        data: {
                            name: $("input[name=name]").val(),
                            level: $("input[name=level]:checked").val(),
                            appid: $("input[name=appid]").val(),
                            appsecret: $("input[name=appsecret]").val(),
                            is_advanced: $("input[name=is_advanced]:checked").val(),
                            username: $("input[name=username]").val(),
                            password: $("input[name=password]").val(),
                            email: $("input[name=email]").val(),
                            original: $("input[name=original]").val(),
                            wechat: $("input[name=wechat]").val(),
                            introduction: $("textarea[name=introduction]").val(),
                            address: $("input[name=address]").val()
                        },
                        beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                            $("button[type=submit]").attr("disabled", "disabled");
                            $("button[type=submit]").text("提交中…");
                        },
                        success: function(data) {
                            noty({
                                type: "success",
                                text: "成功添加 <strong>" + data["name"] + "</strong> 公众号"
                            });
                            window.location.href = "#";
                        },
                        statusCode: {
                            400: function(xhr) {
                                var data = $.parseJSON(xhr.responseText);
                                var errors = {};
                                for (var key in data) {
                                    if (key == "non_field_errors") {
                                        errors["name"] = data[key][0];
                                    } else {
                                        errors[key] = data[key][0];
                                    }
                                }
                                validator.showErrors(errors);
                            }
                        },
                        complete: function() {
                            $("button[type=submit]").removeAttr("disabled");
                            $("button[type=submit]").text("提交");
                        }
                    });
                    return false;
                }
            });
        }
    });

    var OfficialAccountItemEditView = Backbone.View.extend({
        template: _.template(edit_template),
        initialize: function(args) {
            this.official_account = new OfficialAccount({id: args.id});
            this.listenTo(this.official_account, 'change', this.render_official_account);
        },
        /**
         * 渲染编辑公众号页面
         * @returns {OfficialAccountItemEditView}
         */
        render: function() {
            this.$el.html(this.template());
            this.$('input:radio[name=level]').on('change', this, this.toggle_level);
            this.$('input:radio[name=is_advanced]').on('change', this, this.toggle_is_advanced);

            this.render_official_account(this.official_account);
            this.official_account.fetch();
            this.set_validate();

            return this;
        },
        /**
         * 获得当前用户选择的公众号级别
         * @returns {string}
         */
        get_level: function() {
            return this.$el.find('input[name=level]:checked').val();
        },
        /**
         * 判断当前用户是否选择了开启高级支持
         * @returns {boolean}
         */
        get_is_advanced: function() {
            // jQuery-Validation 对 undefined 情况处理不好
            if (this.$el.find('input[name=is_advanced]:checked').val() === '1') {
                return true;
            } else {
                return false;
            }
        },
        /**
         * 切换公众号等级下面的AppID和AppSecret的显示和隐藏
         * @param event
         */
        toggle_level: function(event) {
            if (event.data.$el.find('input[name=level]:checked').val() === '1') {
                event.data.$('#level_div').css('display', 'none');
            } else {
                event.data.$('#level_div').css('display', 'block');
            }
        },
        /**
         * 切换高级支持下面的公众平台用户名和密码的显示和隐藏
         * @param event
         */
        toggle_is_advanced: function(event) {
            if (event.data.$el.find('input[name=is_advanced]:checked').val() === '1') {
                event.data.$('#is_advanced_div').css('display', 'block');
            } else {
                event.data.$('#is_advanced_div').css('display', 'none');
            }
        },
        render_official_account: function(official_account) {
            if (official_account.get('name')) {
                this.$('input[name=name]').val(official_account.get('name'));
                this.$('input[name=level][value=' + official_account.get('level') + ']').prop('checked', true).trigger('change');
                this.$('input[name=appid]').val(official_account.get('appid'));
                this.$('input[name=appsecret]').val(official_account.get('appsecret'));
                if (official_account.get('is_advanced')) {
                    this.$('input[name=is_advanced][value=1]').prop('checked', true).trigger('change');
                } else {
                    this.$('input[name=is_advanced][value=0]').prop('checked', true).trigger('change');
                }
                this.$('input[name=username]').val(official_account.get('username'));
                this.$('input[name=password]').val(official_account.get('password'));
                this.$('input[name=email]').val(official_account.get('email'));
                this.$('input[name=original]').val(official_account.get('original'));
                this.$('input[name=wechat]').val(official_account.get('wechat'));
                this.$('textarea[name=introduction]').val(official_account.get('introduction'));
                this.$('input[name=address]').val(official_account.get('address'));
            }
        },
        /**
         * 设置表单的验证
         */
        set_validate: function() {
            var that = this;
            this.$el.find('#form').validate({
                rules: {
                    name: 'required',
                    level: 'required',
                    appid: {
                        required: function(element) {
                            return that.get_level() == 2 || that.get_level() == 3;
                        }
                    },
                    appsecret: {
                        required: function(element) {
                            return that.get_level() == 2 || that.get_level() == 3;
                        }
                    },
                    is_advanced: 'required',
                    username: {
                        required: function(element) {
                            return that.get_is_advanced();
                        }
                    },
                    password: {
                        required: function(element) {
                            return that.get_is_advanced();
                        }
                    },
                    email: {
                        required: true,
                        email: true
                    },
                    original: 'required',
                    wechat: 'required'
                },
                messages: {
                    name: {
                        required: '公众号名称不能为空'
                    },
                    level: {
                        required: '必须选择一个公众号级别'
                    },
                    appid: {
                        required: '当前公众号级别必须填入App ID'
                    },
                    appsecret: {
                        required: '当前公众号级别必须填入App Secret'
                    },
                    is_advanced: {
                        required: '必选选择是否开启高级支持'
                    },
                    username: {
                        required: '开启高级支持时必须输入公众平台用户名'
                    },
                    password: {
                        required: '开启高级支持时必须输入公众平台密码'
                    },
                    email: {
                        required: '登录邮箱不能为空',
                        email: '登录邮箱不合法'
                    },
                    original: {
                        required: '原始ID不能为空'
                    },
                    wechat: {
                        required: '绑定微信号不能为空'
                    }
                },
                errorClass: 'control-label text-red',
                errorPlacement: function(error, element) {
                    if ($(element).prop('name') == 'level' || $(element).prop('name') == 'is_advanced') {
                        $(element).parent().parent().append(error);
                    } else {
                        error.insertAfter(element);
                    }
                },
                highlight: function(element) {},
                unhighlight: function(element) {},
                submitHandler: function(form) {
                    var validator = this;

                    $.ajax({
                        type: 'PATCH',
                        dataType: 'json',
                        url: '/api/official_account/' + that.official_account.get('id'),
                        cache: false,
                        data: {
                            name: $("input[name=name]").val(),
                            level: $("input[name=level]:checked").val(),
                            appid: $("input[name=appid]").val(),
                            appsecret: $("input[name=appsecret]").val(),
                            is_advanced: $("input[name=is_advanced]:checked").val(),
                            username: $("input[name=username]").val(),
                            password: $("input[name=password]").val(),
                            email: $("input[name=email]").val(),
                            original: $("input[name=original]").val(),
                            wechat: $("input[name=wechat]").val(),
                            introduction: $("textarea[name=introduction]").val(),
                            address: $("input[name=address]").val()
                        },
                        beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                            $("button[type=submit]").attr("disabled", "disabled");
                            $("button[type=submit]").text("提交中…");
                        },
                        success: function(data) {
                            noty({
                                type: "success",
                                text: "成功编辑 <strong>" + data["name"] + "</strong> 公众号"
                            });
                            window.location.href = "#";
                        },
                        statusCode: {
                            400: function(xhr) {
                                var data = $.parseJSON(xhr.responseText);
                                var errors = {};
                                for (var key in data) {
                                    if (key == "non_field_errors") {
                                        errors["name"] = data[key][0];
                                    } else {
                                        errors[key] = data[key][0];
                                    }
                                }
                                validator.showErrors(errors);
                            }
                        },
                        complete: function() {
                            $("button[type=submit]").removeAttr("disabled");
                            $("button[type=submit]").text("提交");
                        }
                    });
                    return false;
                }
            });
        }
    });

    module.exports = {
        'OfficialAccount': OfficialAccount,
        'OfficialAccounts': OfficialAccounts,
        'OfficialAccountItemView': OfficialAccountItemView,
        'OfficialAccountItemDetailView': OfficialAccountItemDetailView,
        'OfficialAccountListView': OfficialAccountListView,
        'OfficialAccountItemAddView': OfficialAccountItemAddView,
        'OfficialAccountItemEditView': OfficialAccountItemEditView
    }
});