$(document).ready(function() {
    var Member = Backbone.Model.extend({
        urlRoot: '/api/member/'
    });
    var Members = Backbone.Collection.extend({
        url: '/api/member/',
        model: Member
    });
    var members = new Members;

    var ConfirmModelView = Backbone.View.extend({
        el: "#confirm-modal",
        events: {
            "click .btn-ok": "run_callback"
        },
        build: function(args) {
            this.$el.find(".model-title").html(args.title);
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
        initialize: function() {
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
        el: $("#member-list-container"),
        template: _.template($("#member-list-template").html()),
        initialize: function() {
            this.listenTo(members, 'add', this.add_with_model);
            members.fetch();
        },
        events: {
            "click .add": "add"
        },
        render: function() {
            this.$el.html(this.template());
            return this;
        },
        add_with_model: function(member) {
            var member_item_view = new MemberItemView({ model: member });
            $(this.el).find(".list").append(member_item_view.render().el);
            return this;
        },
        add: function() {
            this.remove();
        }
    });
    var member_list_view = new MemberListView;
    member_list_view.render();
});