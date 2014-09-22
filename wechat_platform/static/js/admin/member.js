$(document).ready(function() {
    var Member = Backbone.Model.extend({
        urlRoot: '/api/member/'
    });
    var Members = Backbone.Collection.extend({
        url: '/api/member/',
        model: Member
    });
    var members = new Members;

    var Group = Backbone.Model.extend({
        urlRoot: '/api/member/group/'
    });
    var Groups = Backbone.Collection.extend({
        url: '/api/member/group/',
        model: Group
    });
    var groups = new Groups;

    var BreadcrumbView = Backbone.View.extend({
        tagName: "section",
        className: "content-header",
        template: _.template($("#app-breadcrumb-template").html()),
        initialize: function() {},
        render: function(args) {
            this.$el.html(this.template({
                title: args.title,
                subtitle: args.subtitle,
                breadcrumbs: args.breadcrumbs
            }));
            return this;
        }
    });
    var breadcrumb_view = new BreadcrumbView;

    var ConfirmModelView = Backbone.View.extend({
        el: "#confirm-modal",
        events: {
            "click .btn-ok": "run_callback"
        },
        build: function(args) {
            this.$el.find(".modal-title").html(args.title);
            this.$el.find(".modal-body").html("<p>" + args.body + "</p>");
            this.cb = args.cb;
        },
        render: function() {
            this.$el.modal("show");
        },
        close: function() {
            this.$el.modal("hide");
        },
        run_callback: function() {
            this.cb();
            this.$el.modal("hide");
        }
    });
    var confirm_modal_view = new ConfirmModelView;

    var MemberItemView = Backbone.View.extend({
        tagName: "tr",
        template: _.template($("#member-item-template").html()),
        initialize: function(member) {
            this.model = member;
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destroy', this.remove);
        },
        events: {
            "click .edit": "edit_item",
            "click .delete": "delete_item"
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        delete_item: function() {
            var current_model = this.model;
            confirm_modal_view.build({
                cb: function() {
                    current_model.destroy({
                        wait: true,
                        success: function(model, response) {
                            noty({
                                type: "success",
                                text: "成功删除 <strong>" + model.get('username') + "</strong> 用户"
                            });
                        },
                        error: function(model, response) {
                            noty({
                                type: "error",
                                text: "尝试删除 <strong>" + model.get('username') + "</strong> 用户时出错，请重试"
                            });
                        }
                    });
                },
                title: "确认删除",
                body: "请确认您将删除用户名为 <strong><u>" + this.model.get('username') + "</u></strong> 的用户，该操作不可恢复。"
            });
            confirm_modal_view.render();
        }
    });

    var MemberListView = Backbone.View.extend({
        template: _.template($("#member-list-template").html()),
        initialize: function(collection) {
            this.collection = collection;
            this.listenTo(this.collection, 'add', this.add);
        },
        render: function() {
            this.$el.html(this.template());
            _(this.collection.models).each(this.add, this);
            this.collection.fetch();
            return this;
        },
        add: function(member) {
            var member_view = new MemberItemView(member);
            this.$el.find(".list").append(member_view.render().el);
        }
    });
    var member_list_view = new MemberListView(members);

    var MemberItemAddView = Backbone.View.extend({
        template: _.template($("#member-add-user-template").html()),
        initialize: function(args) {
            this.groups = args.groups;
            this.listenTo(this.groups, 'add', this.add_group);
        },
        render: function() {
            this.$el.html(this.template());
            _(this.groups.models).each(this.add_group, this);
            this.groups.fetch();
            this.set_validate();
            return this;
        },
        add_group: function(group) {
            this.$el.find(".groups-checkbox").append("<label class=\"checkbox-inline\"><input type=\"checkbox\" class=\"groups\" name=\"groups\" value=\"" + group.get("id") + "\"> " + group.get("name") + "</label>");
        },
        set_validate: function() {
            this.$el.find("#add-user-form").validate({
                rules: {
                    username: "required",
                    email: {
                        required: true,
                        email: true
                    },
                    nickname: "required",
                    password: "required",
                    password_confirm: {
                        required: true,
                        equalTo: "input[name=password]"
                    },
                    groups: "required"
                },
                messages: {
                    username: {
                        required: "用户名不能为空"
                    },
                    email: {
                        required: "电子邮件不能为空",
                        email: "电子邮件地址不合法"
                    },
                    nickname: {
                        required: "昵称不能为空"
                    },
                    password: {
                        required: "密码不能为空"
                    },
                    password_confirm: {
                        required: "确认密码不能为空",
                        equalTo: "两次密码输入不一致"
                    },
                    groups: {
                        required: "最少选择一个用户组"
                    }
                },
                errorClass: 'control-label text-red',
                errorPlacement: function(error, element) {
                    if ($(element).hasClass("groups")) {
                        error.insertAfter($(element).parent().parent().parent().find("span"));
                    } else {
                        error.insertAfter(element);
                    }
                },
                highlight: function(element) {},
                unhighlight: function(element) {},
                submitHandler: function(form) {
                    var validator = this;

                    $.ajax({
                        type: "POST",
                        dataType: "json",
                        url: "/api/member/",
                        cache: false,
                        data: {
                            username: $("input[name=username]").val(),
                            email: $("input[name=email]").val(),
                            nickname: $("input[name=nickname]").val(),
                            password: $("input[name=password]").val(),
                            groups: $("input[name=groups]:checked").map(function() {
                                return $(this).val();
                            }).get()
                        },
                        beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                            $("button[type=submit]").attr("disabled", "disabled");
                            $("button[type=submit]").text("提交中…");
                        },
                        success: function(data) {
                            noty({
                                type: "success",
                                text: "成功添加 " + data["username"] + " 用户"
                            });
                            window.location.href = "#";
                        },
                        statusCode: {
                            400: function(xhr) {
                                var data = $.parseJSON(xhr.responseText);
                                var errors = {};
                                for (var key in data) {
                                    if (key == "non_field_errors") {
                                        errors["username"] = data[key][0];
                                    } else {
                                        errors[key] = data[key][0];
                                    }
                                }
                                validator.showErrors(errors);
                            }
                        },
                        complete: function() {
                            $("button[type=submit]").removeAttr("disabled");
                            $("button[type=submit]").text("添加用户");
                        }
                    });
                    return false;
                }
            });
        }
    });
    var member_item_add_view = new MemberItemAddView({ groups: groups });

    var AppView = Backbone.View.extend({
        el: $("#container"),
        template_container: _.template($("#app-template").html()),
        template_header_list: _.template($("#app-header-list-template").html()),
        template_header_add_user: _.template($("#app-header-add-user-template").html()),
        initialize: function() {
            this.render();
            this.breadcrumb = this.$el.find(".right-side");
            this.header = this.$el.find("#header");
            this.content = this.$el.find("#content");
        },
        render: function() {
            this.$el.html(this.template_container());
        },

        set_breadcrumb: function(title, subtitle, breadcrumbs) {
            this.breadcrumb.prepend(breadcrumb_view.render({
                title: title,
                subtitle: subtitle,
                breadcrumbs: breadcrumbs
            }).el);
        },
        set_header: function(html) {
            this.header.html(html);
        },
        set_content: function(html) {
            this.content.html(html);
        },

        default_interface: function() {
            this.set_breadcrumb('用户', '管理用户列表', [{title:'用户', url:'#'}]);
            this.set_header(this.template_header_list());
            this.set_content(member_list_view.render().el);
        },
        add_user_interface: function() {
            this.set_breadcrumb('添加用户', '添加一个新的用户', [{title:'用户', url:'#'},{title:'添加用户', url:'#/add_user'}]);
            this.set_header(this.template_header_add_user());
            this.set_content(member_item_add_view.render().el);
        }
    });
    var app_view = new AppView;

    var AppRouter = Backbone.Router.extend({
        routes: {
            "add_user": "add_user",
            "*actions": "default_router"
        },
        add_user: function() {
            app_view.add_user_interface();
        },
        default_router: function(actions) {
            app_view.default_interface();
        }
    });
    var app_router = new AppRouter;
    Backbone.history.start();
});