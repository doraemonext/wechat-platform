$(document).ready(function() {
    var Member = Backbone.Model.extend({
        urlRoot: '/api/member/'
    });
    var Members = Backbone.Collection.extend({
        url: '/api/member/',
        model: Member
    });
    var members = new Members;

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
            this.render();
            this.listenTo(this.collection, 'add', this.add);
            this.collection.fetch();
        },
        render: function() {
            this.$el.html(this.template());
            _(this.collection.models).each(this.add, this);
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
        initialize: function() {
        },
        render: function() {
            this.$el.html(this.template());
            return this;
        }
    });
    var member_item_add_view = new MemberItemAddView;

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