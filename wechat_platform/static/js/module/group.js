define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var ConfirmModal = require('helper.confirm-modal');
    require('jquery-validate');
    require('jquery-cookie');

    var item_template = require('text!templates/group/item.html');
    var list_template = require('text!templates/group/list.html');
    var detail_template = require('text!templates/group/detail.html');
    var add_template = require('text!templates/group/edit.html');
    var edit_template = require('text!templates/group/edit.html');

    var confirm_modal_view = new ConfirmModal;

    var Group = Backbone.Model.extend({
        urlRoot: '/api/group/'
    });
    var Groups = Backbone.Collection.extend({
        url: '/api/group/',
        model: Group
    });

    var GroupItemView = Backbone.View.extend({
        tagName: 'tr',
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
                                text: "成功删除 <strong>" + model.get('name') + "</strong> 用户组"
                            });
                        },
                        error: function(model, response) {
                            noty({
                                type: "error",
                                text: "尝试删除 <strong>" + model.get('name') + "</strong> 用户组时出错，请重试"
                            });
                        }
                    });
                },
                title: "确认删除",
                body: "请确认您将删除 <strong><u>" + this.model.get('name') + "</u></strong> 用户组，该操作不可恢复。"
            });
        }
    });

    var GroupItemDetailView = Backbone.View.extend({
        template: _.template(detail_template),
        initialize: function(args) {
            this.group = new Group({id: args.id});
            this.listenTo(this.group, 'change', this.render_group)
        },
        events: {
            'click .delete': 'delete_item'
        },
        render: function() {
            this.$el.html(this.template({id: this.group.id}));
            this.render_group(this.group);
            this.group.fetch();
            return this;
        },
        render_group: function(group) {
            this.$('#group-name').html(group.get('name'));
        },
        delete_item: function() {
            var current_model = this.group;
            confirm_modal_view.show({
                cb: function() {
                    current_model.destroy({
                        wait: true,
                        success: function(model, response) {
                            noty({
                                type: "success",
                                text: "成功删除 <strong>" + model.get('name') + "</strong> 用户组"
                            });
                            window.location.href = '#';
                        },
                        error: function(model, response) {
                            noty({
                                type: "error",
                                text: "尝试删除 <strong>" + model.get('name') + "</strong> 用户组时出错，请重试"
                            });
                        }
                    });
                },
                title: "确认删除",
                body: "请确认您将删除 <strong><u>" + this.group.get('name') + "</u></strong> 用户组，该操作不可恢复。"
            });
        }
    });

    var GroupListView = Backbone.View.extend({
        template: _.template(list_template),
        initialize: function() {
            this.collection = new Groups;
            this.listenTo(this.collection, 'add', this.add);
        },
        render: function() {
            this.$el.html(this.template());
            _(this.collection.models).each(this.add, this);
            this.collection.fetch();
            return this;
        },
        add: function(group) {
            var group_view = new GroupItemView({model: group});
            this.$(".list").append(group_view.render().el);
        }
    });

    var GroupItemAddView = Backbone.View.extend({
        template: _.template(add_template),
        initialize: function() {},
        /**
         * 渲染添加用户组页面
         * @returns {GroupItemAddView}
         */
        render: function() {
            this.$el.html(this.template());
            this.set_validate();
            return this;
        },
        /**
         * 设置表单的验证
         */
        set_validate: function() {
            var that = this;
            this.$el.find('#form').validate({
                rules: {
                    name: 'required'
                },
                messages: {
                    name: {
                        required: '用户组名称不能为空'
                    }
                },
                errorClass: 'control-label text-red',
                highlight: function(element) {},
                unhighlight: function(element) {},
                submitHandler: function(form) {
                    var validator = this;

                    $.ajax({
                        type: 'POST',
                        dataType: 'json',
                        url: '/api/group/',
                        cache: false,
                        data: {
                            name: $("input[name=name]").val()
                        },
                        beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                            $("button[type=submit]").attr("disabled", "disabled");
                            $("button[type=submit]").text("提交中…");
                        },
                        success: function(data) {
                            noty({
                                type: "success",
                                text: "成功添加 <strong>" + data["name"] + "</strong> 用户组"
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

    var GroupItemEditView = Backbone.View.extend({
        template: _.template(edit_template),
        initialize: function(args) {
            this.group = new Group({id: args.id});
            this.listenTo(this.group, 'change', this.render_group);
        },
        /**
         * 渲染编辑用户组页面
         * @returns {GroupItemEditView}
         */
        render: function() {
            this.$el.html(this.template());

            this.render_group(this.group);
            this.group.fetch();
            this.set_validate();

            return this;
        },
        render_group: function(group) {
            if (group.get('name')) {
                this.$('input[name=name]').val(group.get('name'));
            }
        },
        /**
         * 设置表单的验证
         */
        set_validate: function() {
            var that = this;
            this.$el.find('#form').validate({
                rules: {
                    name: 'required'
                },
                messages: {
                    name: {
                        required: '用户组名称不能为空'
                    }
                },
                errorClass: 'control-label text-red',
                highlight: function(element) {},
                unhighlight: function(element) {},
                submitHandler: function(form) {
                    var validator = this;

                    $.ajax({
                        type: 'PATCH',
                        dataType: 'json',
                        url: '/api/group/' + that.group.get('id'),
                        cache: false,
                        data: {
                            name: $("input[name=name]").val()
                        },
                        beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                            $("button[type=submit]").attr("disabled", "disabled");
                            $("button[type=submit]").text("提交中…");
                        },
                        success: function(data) {
                            noty({
                                type: "success",
                                text: "成功编辑 <strong>" + data["name"] + "</strong> 用户组"
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
        'Group': Group,
        'Groups': Groups,
        'GroupItemView': GroupItemView,
        'GroupItemDetailView': GroupItemDetailView,
        'GroupListView': GroupListView,
        'GroupItemAddView': GroupItemAddView,
        'GroupItemEditView': GroupItemEditView
    }
});