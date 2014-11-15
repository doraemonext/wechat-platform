define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var ConfirmModal = require('helper.confirm-modal');
    require('spin');
    require('jquery-validate');
    require('jquery-cookie');
    require('backbone-paginator');

    var item_template = require('text!templates/library/music/item.html');
    var list_template = require('text!templates/library/music/list.html');
    //var detail_template = require('text!templates/library/music/detail.html');
    var add_template = require('text!templates/library/music/edit.html');
    //var edit_template = require('text!templates/library/music/edit.html');

    var confirm_modal_view = new ConfirmModal;

    var LibraryMusicModel = Backbone.Model.extend({
        urlRoot: '/api/library/music/'
    });
    var LibraryMusicCollection = Backbone.PageableCollection.extend({
        url: '/api/library/music/?official_account=' + $('#current-official-account').val(),
        model: LibraryMusicModel,
        state: {
            pageSize: 5
        },
        parseRecords: function (resp) {
            return resp.results;
        },
        parseState: function (resp, queryParams, state, options) {
            return { totalRecords: resp.count };
        }
    });

    var LibraryMusicItemView = Backbone.View.extend({
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
                                text: "成功删除 <strong>" + model.get('title') + "</strong> 音乐素材"
                            });
                        },
                        error: function(model, response) {
                            noty({
                                type: "error",
                                text: "尝试删除 <strong>" + model.get('title') + "</strong> 音乐素材时出错，请重试"
                            });
                        }
                    });
                },
                title: "确认删除",
                body: "请确认您将删除 <strong><u>" + this.model.get('title') + "</u></strong> 音乐素材，该操作不可恢复。"
            });
        }
    });
    var LibraryMusicListView = Backbone.View.extend({
        template: _.template(list_template),
        events: {
            "click .pagination-previous": "pagination_previous",
            "click .pagination-next": "pagination_next",
            "click .goto-area button ": "goto_area",
            "keyup .goto-area input": "goto_area_enter"
        },
        initialize: function() {
            this.collection = new LibraryMusicCollection;
            this.listenTo(this.collection, 'add', this.add);
            this.listenTo(this.collection, 'reset', this.reset);
        },
        render: function() {
            var that = this;
            this.$el.html(this.template());
            _(this.collection.models).each(this.add, this);
            this.collection.fetch({
                success: function(collection) {
                    if (!collection.length) {
                        that.$('#no-library-music').css('display', 'block');
                    }
                    that._adjust_pagination();
                }
            });
            return this;
        },
        add: function (music) {
            var library_music_view = new LibraryMusicItemView({model: music});
            this.$('#no-library-music').css('display', 'none');
            this.$(".list").append(library_music_view.render().el);
        },
        reset: function() {
            this.$(".list").html('');
        },
        pagination_previous: function () {
            this.collection.reset();
            this.collection.getPreviousPage().done(this._adjust_pagination());
        },
        pagination_next: function () {
            this.collection.reset();
            this.collection.getNextPage().done(this._adjust_pagination());
        },
        goto_area: function () {
            var page = this.$('.goto-area input[type=text]').val();
            if ($.isNumeric(page) && parseInt(page) > 0 && parseInt(page) <= this.collection.state.totalPages) {
                this.collection.reset();
                this.$('.goto-area input[type=text]').val('');
                this.collection.getPage(parseInt(page)).done(this._adjust_pagination());
            } else {
                noty({
                    type: "error",
                    text: "您输入的跳转页数非法"
                });
            }
        },
        goto_area_enter: function (event) {
            if (event.keyCode == 13) {
                this.$('.goto-area button').click();
            }
        },
        /**
         * 根据当前页面状态调整页码的显示
         */
        _adjust_pagination: function () {
            this.$('.page').html(this.collection.state.currentPage + ' / ' + this.collection.state.totalPages);
            if (this.collection.hasPreviousPage()) {
                this.$('.pagination-previous').css('display', 'inline');
            } else {
                this.$('.pagination-previous').css('display', 'none');
            }
            if (this.collection.hasNextPage()) {
                this.$('.pagination-next').css('display', 'inline');
            } else {
                this.$('.pagination-next').css('display', 'none');
            }
        }
    });

    var LibraryMusicItemAddView = Backbone.View.extend({
        template: _.template(add_template),
        initialize: function() {},
        /**
         * 渲染添加音乐素材页面
         * @returns {LibraryMusicItemAddView}
         */
        render: function() {
            this.$el.html(this.template());
            /*this.set_validate();
            this.$('input[name=level]').on('change', this, this.toggle_level);
            this.$('input[name=is_advanced]').on('change', this, this.toggle_is_advanced);*/
            return this;
        },
        /**
         * 设置表单的验证
         */
        /*set_validate: function() {
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
        }*/
    });

    module.exports = {
        'LibraryMusicModel': LibraryMusicModel,
        'LibraryMusicCollection': LibraryMusicCollection,
        'LibraryMusicItemView': LibraryMusicItemView,
        'LibraryMusicListView': LibraryMusicListView,
        'LibraryMusicItemAddView': LibraryMusicItemAddView
    }
});