define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var ConfirmModal = require('helper.confirm-modal');
    var confirm_modal_view = new ConfirmModal;
    var item_template = require('text!templates/official_account/item.html');
    var list_template = require('text!templates/official_account/list.html');
    var detail_template = require('text!templates/official_account/detail.html');

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
            this.$el.html(this.template());
            _(this.collection.models).each(this.add, this);
            this.collection.fetch();
            return this;
        },
        add: function(official_account) {
            var official_account_view = new OfficialAccountItemView({model: official_account});
            this.$el.find(".list").append(official_account_view.render().el);
        }
    });

    module.exports = {
        'OfficialAccount': OfficialAccount,
        'OfficialAccounts': OfficialAccounts,
        'OfficialAccountItemView': OfficialAccountItemView,
        'OfficialAccountItemDetailView': OfficialAccountItemDetailView,
        'OfficialAccountListView': OfficialAccountListView
    }
});