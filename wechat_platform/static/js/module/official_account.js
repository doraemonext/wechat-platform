define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var ConfirmModal = require('helper.confirm-modal');
    var confirm_modal_view = new ConfirmModal;
    var item_template = require('text!templates/official_account/item.html');
    var list_template = require('text!templates/official_account/list.html');

    var OfficialAccount = Backbone.Model.extend({
        urlRoot: '/api/official_account/'
    });
    var OfficialAccounts = Backbone.Collection.extend({
        url: '/api/official_account/',
        model: OfficialAccount
    });

    var OfficialAccountItemView = Backbone.View.extend({
        template: _.template(item_template),
        initialize: function(official_account) {
            this.model = official_account;
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
                body: "请确认您将删除 <strong><u>" + this.model.get('username') + "</u></strong> 公众号，该操作不可恢复。"
            });
        }
    });

    var OfficialAccountListView = Backbone.View.extend({
        template: _.template(list_template),
        initialize: function() {
            this.collection = new OfficialAccounts;
            this.listenTo(this.collection, 'add', this.add);
        },
        render: function() {
            this.$el.html(this.template());
            _(this.collection.models).each(this.add, this);
            this.collection.fetch();
            return this;
        },
        add: function(official_account) {
            var official_account_view = new OfficialAccountItemView(official_account);
            this.$el.find(".list").append(official_account_view.render().el);
        }
    });

    module.exports = {
        'OfficialAccount': OfficialAccount,
        'OfficialAccounts': OfficialAccounts,
        'OfficialAccountItemView': OfficialAccountItemView,
        'OfficialAccountListView': OfficialAccountListView
    }
});