define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var ConfirmModal = require('helper.confirm-modal');
    var CKEDITOR = require('ckeditor');
    require('spin');
    require('jquery-validate');
    require('jquery-cookie');
    require('jquery-form');
    require('backbone-paginator');

    var item_template = require('text!templates/library/news/item.html');
    var multi_item_template = require('text!templates/library/news/multi_item.html');
    var list_template = require('text!templates/library/news/list.html');
    var add_template = require('text!templates/library/news/edit.html');
    var add_sub_news_template = require('text!templates/library/news/add_sub_news.html');
    var edit_template = require('text!templates/library/news/edit.html');

    var confirm_modal_view = new ConfirmModal;

    var MediaModel = Backbone.Model.extend({
        urlRoot: '/api/filetranslator/'
    });
    var LibraryNewsModel = Backbone.Model.extend({
        urlRoot: '/api/library/news/'
    });
    var LibraryNewsCollection = Backbone.PageableCollection.extend({
        url: '/api/library/news/?official_account=' + $('#current-official-account').val(),
        model: LibraryNewsModel,
        state: {
            pageSize: 12
        },
        parseRecords: function (resp) {
            return resp.results;
        },
        parseState: function (resp, queryParams, state, options) {
            return { totalRecords: resp.count };
        }
    });

    var LibraryNewsItemView = Backbone.View.extend({
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
                                text: "成功删除 <strong>" + model.get('title') + "</strong> 图文素材"
                            });
                        },
                        error: function(model, response) {
                            noty({
                                type: "error",
                                text: "尝试删除 <strong>" + model.get('title') + "</strong> 图文素材时出错，请重试"
                            });
                        }
                    });
                },
                title: "确认删除",
                body: "请确认您将删除 <strong><u>" + this.model.get('title') + "</u></strong> 图文素材，该操作不可恢复。"
            });
        }
    });
    var LibraryNewsMultiItemView = Backbone.View.extend({
        template: _.template(multi_item_template),
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
                                text: "成功删除 <strong>" + model.get('title') + "</strong> 图文素材"
                            });
                        },
                        error: function(model, response) {
                            noty({
                                type: "error",
                                text: "尝试删除 <strong>" + model.get('title') + "</strong> 图文素材时出错，请重试"
                            });
                        }
                    });
                },
                title: "确认删除",
                body: "请确认您将删除 <strong><u>" + this.model.get('title') + "</u></strong> 图文素材，该操作不可恢复。"
            });
        }
    });
    var LibraryNewsListView = Backbone.View.extend({
        template: _.template(list_template),
        events: {
            "click .pagination-previous": "pagination_previous",
            "click .pagination-next": "pagination_next",
            "click .goto-area button ": "goto_area",
            "keyup .goto-area input": "goto_area_enter"
        },
        initialize: function() {
            this.collection = new LibraryNewsCollection;
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
                        that.$('#no-library-news').css('display', 'block');
                    }
                    that._adjust_pagination();
                }
            });
            return this;
        },
        add: function (news) {
            var library_news_view;
            if (news.get('multi_item').length > 1) {
                library_news_view = new LibraryNewsMultiItemView({model: news});
            } else {
                library_news_view = new LibraryNewsItemView({model: news});
            }
            this.$('#no-library-news').css('display', 'none');

            // 计算下一次应该在哪一列插入图文
            var col_length = [
                this.$('#news-col-0').children().length,
                this.$('#news-col-1').children().length,
                this.$('#news-col-2').children().length
            ];
            var min_length_pos = 0;
            for (var i = 0; i < col_length.length; i++) {
                if (col_length[i] < col_length[min_length_pos]) {
                    min_length_pos = i;
                }
            }
            this.$('#news-col-' + min_length_pos).append(library_news_view.render().el);
            this.$("span[data-toggle=tooltip]").tooltip({
                container: 'body',
                html: true,
                template: '<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
            })
        },
        reset: function() {
            this.$("#news-col-0").html('');
            this.$("#news-col-1").html('');
            this.$("#news-col-2").html('');
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

    var LibraryNewsItemAddView = Backbone.View.extend({
        template: _.template(add_template),
        initialize: function() {
            localStorage.setItem('news_current', '0');
            localStorage.setItem('news_array', JSON.stringify([this._get_empty_news()]));
        },
        events: {
            "click #add_sub_news": "add_sub_news",
            "click .edit": "edit_sub_news",
            "click .delete": "delete_sub_news"
        },
        /**
         * 渲染添加图文素材页面
         * @returns {LibraryNewsItemAddView}
         */
        render: function () {
            this.$el.html(this.template());
            this.$('input:radio[name="pattern"]').on('change', this, this._trigger_pattern);

            var news_current = this._get_news_current();
            var news_array = this._get_news_array();
            for (var i = 1; i < news_array.length; i++) {  // 注意因为至少存在一条图文，默认图文已经在模板中写好，所以从 i=1 开始动态添加
                this.add_sub_news();
            }
            this._update_editor(news_current);
            this.set_validate();
            return this;
        },
        /**
         * 当点击添加子图文按钮时触发该函数
         */
        add_sub_news: function () {
            var news_array = this._get_news_array();
            var news_sum = news_array.length;

            if (news_sum >= 10) {
                noty({
                    type: "error",
                    text: "您最多只能添加十条图文"
                });
                return;
            }
            this.$('.appmsg_content').append(_.template(add_sub_news_template)({'id': news_sum}));
            news_array.push(this._get_empty_news());
            this._set_news_array(news_array);
        },
        /**
         * 当点击编辑子图文按钮时触发该函数
         * @param event
         */
        edit_sub_news: function (event) {
            var news_array = this._get_news_array();
            var news_id = parseInt($(event.currentTarget).attr('data-news-id'));

            this._set_news_current(news_id);
            this._update_editor(news_id);
        },
        /**
         * 当点击删除子图文按钮时触发该函数
         * @param event
         */
        delete_sub_news: function (event) {
            var news_array = this._get_news_array();
            var news_current = this._get_news_current();
            var news_id = parseInt($(event.currentTarget).attr('data-news-id'));

            this.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ')').remove();
            this._update_preview_area();
            news_array.splice(news_id, 1);
            if ((news_id == news_current && news_current >= news_array.length) || (news_id < news_current)) {
                news_current--;
            }
            this._set_news_current(news_current);
            this._set_news_array(news_array);
            this._update_editor(news_current);
        },
        /**
         * Hack: 修正首图文无法在渲染时获得事件绑定问题，由上层在HTML渲染好后负责调用
         */
        fix_ckeditor: function () {
            this._update_editor(this._get_news_current());
        },
        /**
         * 更新所有左侧预览图文中的序号 (用于对左侧预览图文顺序变动后)
         * @private
         */
        _update_preview_area: function () {
            this.$('.appmsg_content .js_appmsg_item').each(function (index) {
                $(this).find('.edit').attr('data-news-id', index);
                $(this).find('.delete').attr('data-news-id', index);
            });
        },
        /**
         * 更新编辑表单中的所有信息并且移动到适当位置
         * @param news_id {Number}
         * @private
         */
        _update_editor: function (news_id) {
            // 更新编辑框的位置
            if (news_id == 0) {
                this.$('#editor').css('margin-top', '0');
            } else {
                this.$('#editor').css('margin-top', 79 + news_id * 119 + 'px');
            }

            this._clear_editor_error_info();
            this._update_editor_title(news_id);
            this._update_editor_author(news_id);
            this._update_editor_picture(news_id);
            this._update_editor_description(news_id);
            this._update_editor_content(news_id);
            this._update_editor_url(news_id);
            this._update_editor_pattern(news_id);
            this._update_editor_from_url(news_id);
        },
        _update_editor_title: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('input[name="title"]').val(news_array[news_id].title);
            this.$('input[name="title"]').unbind('input propertychange change');
            this.$('input[name="title"]').bind('input propertychange', function () {
                that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') .appmsg_title a').html($(this).val());
            });
            this.$('input[name="title"]').bind('change', function () {
                news_array = that._get_news_array();
                news_array[news_id].title = $(this).val();
                that._set_news_array(news_array);
            });
        },
        _update_editor_author: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('input[name="author"]').val(news_array[news_id].author);
            this.$('input[name="author"]').unbind('change');
            this.$('input[name="author"]').bind('change', function () {
                news_array = that._get_news_array();
                news_array[news_id].author = $(this).val();
                that._set_news_array(news_array);
            });
        },
        _update_editor_picture: function (news_id) {
            this.set_file_upload(news_id);
        },
        _update_editor_description: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('textarea[name="description"]').val(news_array[news_id].description);
            this.$('textarea[name="description"]').unbind('change');
            this.$('textarea[name="description"]').bind('change', function () {
                news_array = that._get_news_array();
                news_array[news_id].description = $(this).val();
                that._set_news_array(news_array);
            });
        },
        _update_editor_content: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('textarea[name="news_content"]').val(news_array[news_id].content);
            if (CKEDITOR.instances.hasOwnProperty('news_content')) {
                CKEDITOR.instances.news_content.setData(news_array[news_id].content);
            }
            if (CKEDITOR.instances.hasOwnProperty('news_content')) {
                var editor = CKEDITOR.instances.news_content;
                editor.on('change', function (event) {
                    var news_array = that._get_news_array();
                    var news_current = that._get_news_current();
                    news_array[news_current].content = editor.getData();
                    that._set_news_array(news_array);
                });
            }
        },
        _update_editor_url: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('input[name="url"]').val(news_array[news_id].url);
            this.$('input[name="url"]').unbind('change');
            this.$('input[name="url"]').bind('change', function () {
                news_array = that._get_news_array();
                news_array[news_id].url = $(this).val();
                that._set_news_array(news_array);
            });
        },
        _update_editor_pattern: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            if (news_array[news_id].pattern == 'text') {
                this.$('input:radio[name="pattern"][value="text"]').prop('checked', true).trigger('change');
            } else {
                this.$('input:radio[name="pattern"][value="url"]').prop('checked', true).trigger('change');
            }
        },
        _update_editor_from_url: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('input[name="from_url"]').val(news_array[news_id].from_url);
            this.$('input[name="from_url"]').unbind('change');
            this.$('input[name="from_url"]').bind('change', function () {
                news_array = that._get_news_array();
                news_array[news_id].from_url = $(this).val();
                that._set_news_array(news_array);
            });
        },
        /**
         * 设置编辑框的验证错误信息
         * @param data 验证错误信息
         * @private
         */
        _set_editor_error_info: function (data) {
            if (data.title) {
                this.$('#title_error').html(data.title[0]);
            }
            if (data.author) {
                this.$('#author_error').html(data.author[0]);
            }
            if (data.description) {
                this.$('#description_error').html(data.description[0]);
            }
            if (data.content) {
                this.$('#content_error').html(data.content[0]);
            }
            if (data.url) {
                this.$('#content_error').html(data.url[0]);
            }
            if (data.from_url) {
                this.$('#from_url_error').html(data.from_url[0]);
            }
        },
        /**
         * 清除编辑框的验证错误信息
         * @private
         */
        _clear_editor_error_info: function () {
            this.$('#title_error').html('');
            this.$('#author_error').html('');
            this.$('#description_error').html('');
            this.$('#content_error').html('');
            this.$('#from_url_error').html('');
        },
        /**
         * 触发内容展现方式 radio 时触发此函数
         * @param event
         * @private
         */
        _trigger_pattern: function (event) {
            var news_array = event.data._get_news_array();
            var news_current = event.data._get_news_current();
            if (event.data.$el.find('input[name="pattern"]:checked').val() === 'text') {
                event.data.$('#text_content').css('display', 'block');
                event.data.$('#url_content').css('display', 'none');
                news_array[news_current].pattern = 'text';
            } else {
                event.data.$('#text_content').css('display', 'none');
                event.data.$('#url_content').css('display', 'block');
                news_array[news_current].pattern = 'url';
            }
            news_array = event.data._set_news_array(news_array);
        },
        /**
         * 返回 localStorage 中存储的当前正在编辑的图文序号
         * @returns {Number}
         * @private
         */
        _get_news_current: function () {
            return parseInt(localStorage.getItem('news_current'));
        },
        /**
         * 设置 localStorage 中存储的当前正在编辑的图文序号
         * @param news_id {Number}
         * @private
         */
        _set_news_current: function (news_id) {
            localStorage.setItem('news_current', news_id);
        },
        /**
         * 返回 localStorage 中存储的当前图文信息数组
         * @returns {*}
         * @private
         */
        _get_news_array: function () {
            return JSON.parse(localStorage.getItem('news_array'));
        },
        /**
         * 设置 localStorage 中的当前图文信息数组
         * @param news {Array}
         * @private
         */
        _set_news_array: function (news) {
            localStorage.setItem('news_array', JSON.stringify(news));
        },
        /**
         * 生成一个空的 news 对象, 默认使用文本内容
         * @returns {{title: string, description: string, picture: string, author: string, pattern: string, content: string, url: string, from_url: string}}
         * @private
         */
        _get_empty_news: function () {
            return {
                title: '',
                description: '',
                picture: '',
                author: '',
                pattern: 'text',
                content: '',
                url: '',
                from_url: ''
            }
        },
        /**
         * 删除系统媒体文件
         * @param key 媒体文件标识符 key
         * @returns {*}
         */
        delete_media_file: function (key) {
            return $.ajax({
                url: '/api/filetranslator/' + key + '/',
                type: 'DELETE',
                async: false,
                error: function () {
                    noty({
                        type: "error",
                        text: "删除文件时出错, 请重试"
                    });
                }
            });
        },
        /**
         * 设置页面中的文件上传组件
         */
        set_file_upload: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            var info = this.$('#upload_picture .upload-info');
            var progress = this.$('#upload_picture .upload-progress');
            var btn = this.$('#upload_picture .upload-button');

            info.set_content = function (url, key) {
                var content = '<div class="news-picture"><img class="img-responsive img-rounded" src="' + url + '" ></div>';
                content += '<div class="news-picture-opr"><strong><a class="delete-media" data-key="' + key + '" href="javascript:void(0)">删除该文件</a></strong></div>';
                content += '<div class="clearfix"></div>';
                $(this).html(content);
                $(this).find('.delete-media').click(function () {
                    var key = $(this).attr('data-key');
                    that.delete_media_file(key).success(function () {
                        btn.display_select_upload();
                        info.hide();
                        news_array[news_id].picture = '';
                        that._set_news_array(news_array);

                        // 当删除首图文图片时的同时恢复左侧预览图为默认图片
                        if (news_id == 0) {
                            that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb_wrp img').attr('src', '');
                            that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb').css('display', 'block');
                            that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb_wrp img').css('display', 'none');
                        } else {
                            that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') img').attr('src', '');
                            that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') .appmsg_thumb').css('display', 'block');
                            that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') img').css('display', 'none');
                        }
                    });
                });

                // 当上传图片成功时设置左侧预览图为对应图片
                if (news_id == 0) {
                    that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb_wrp img').attr('src', url);
                    that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb').css('display', 'none');
                    that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb_wrp img').css('display', 'block');
                } else {
                    that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') img').attr('src', url);
                    that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') .appmsg_thumb').css('display', 'none');
                    that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') img').css('display', 'block');
                }
            };
            info.set_error_content = function (content) {
                $(this).html('<span class="text-red">上传失败：' + content + '</span>');
            };
            progress.set_progress = function (percent) {
                progress.find('.progress-bar').css('width', percent + '%');
                progress.find('.progress-bar').attr('aria-valuenow', percent);
                progress.find('.progress-bar').html(percent + '%');
            };
            btn.display_select_upload = function () {
                $(this).find('input').prop('disabled', false);
                $(this).removeClass('disabled');
                $(this).find('span').html('上传');
            };
            btn.display_uploading = function () {
                $(this).find('input').prop('disabled', true);
                $(this).addClass('disabled');
                $(this).find('span').html('上传中...');
            };
            btn.display_restart_upload = function () {
                $(this).find('input').prop('disabled', false);
                $(this).removeClass('disabled');
                $(this).find('span').html('重新上传');
            };

            this.$('input[id="picture"]').unbind('click change');
            if (news_array[news_id].picture.length > 0) {  // 当该子图文已经上传过封面图片时，直接请求并显示，否则重建上传框
                btn.display_restart_upload();
                progress.hide();
                $.ajax({
                    url: '/api/filetranslator/' + news_array[news_id].picture + '/',
                    type: 'GET',
                    dataType: 'json',
                    success: function (data) {
                        info.set_content(data['url'], data['key']);
                        info.show();
                    }
                });
            } else {
                info.html('');
                info.hide();
                progress.set_progress(0);
                progress.hide();
                btn.display_select_upload();
            }

            this.$('input[id="picture"]').click(function () {  // 此处为两次提交重复文件不响应 change 的解决方案
                $(this).val('');
            });
            this.$('input[id="picture"]').change(function () {
                var news_array = that._get_news_array();
                that.$('#upload_picture form').ajaxSubmit({
                    dataType: 'json',
                    data: {
                        'official_account': $('#current-official-account').val(),
                        'type': 1
                    },
                    beforeSend: function (xhr) {
                        var origin_key = news_array[news_id].picture;
                        if (origin_key.length > 0) {  // 当原先存在封面图片时先删除原先的
                            that.delete_media_file(origin_key).success(function () {
                                news_array[news_id].picture = '';
                                that._set_news_array(news_array);
                            });
                        }

                        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                        btn.display_uploading();
                        progress.set_progress(0);
                        progress.show();
                        info.hide();
                    },
                    uploadProgress: function (event, position, total, percentComplete) {
                        progress.set_progress(percentComplete);
                    },
                    success: function (data) {
                        news_array[news_id].picture = data['key'];
                        that._set_news_array(news_array);

                        btn.display_restart_upload();
                        progress.hide();
                        info.set_content(data['url'], data['key']);
                        info.show();
                    },
                    statusCode: {
                        400: function(xhr) {
                            var data = $.parseJSON(xhr.responseText);
                            for (var key in data) {
                                btn.display_select_upload();
                                progress.hide();
                                info.set_error_content(data[key][0]);
                                info.show();
                                break;  // 直接针对第一条错误给出提示, 其他忽略
                            }
                        },
                        500: function(xhr) {
                            btn.display_select_upload();
                            progress.hide();
                            info.hide();
                            noty({
                                type: "error",
                                text: "服务器内部出错, 请重试"
                            });
                        }
                    },
                    error: function(xhr) {
                        if (xhr.status != 400 && xhr.status != 500) {
                            btn.display_select_upload();
                            progress.hide();
                            if (xhr.status == 413) {
                                info.set_error_content('错误' + xhr.status + ' - 请求数据过长，请尝试增大服务器最大上传限制');
                            } else {
                                info.set_error_content('错误' + xhr.status);
                            }
                            info.show();
                        }
                    }
                });
            });
        },
        /**
         * 设置表单的验证
         */
        set_validate: function() {
            var that = this;
            this.$('#submit_news').bind('click', function () {
                that._clear_editor_error_info();

                var news_array = that._get_news_array();
                var news_current = that._get_news_current();
                var error = {};
                var error_flag = false;

                for (var i = 0; i < news_array.length; i++) {
                    error.current_position = i;
                    if (news_array[i].title.length == 0) {
                        error.title = ['图文标题不能为空'];
                        error_flag = true;
                    } else if (news_array[i].title.length > 100) {
                        error.title = ['图文标题最长为 100 字符'];
                        error_flag = true;
                    }

                    if (news_array[i].author.length > 100) {
                        error.author = ['作者最长为 100 字符'];
                        error_flag = true;
                    }

                    if (news_array[i].pattern == 'text' && news_array[i].content == 0) {
                        error.content = ['图文内容不能为空'];
                        error_flag = true;
                    } else if (news_array[i].pattern == 'url' && news_array[i].url == 0) {
                        error.url = ['跳转链接不能为空'];
                        error_flag = true;
                    }

                    if (error_flag) {
                        break;
                    }
                }

                if (error_flag) {
                    that._set_news_current(error.current_position);
                    that._update_editor(error.current_position);
                    that._set_editor_error_info(error);
                    noty({
                        type: 'error',
                        text: '验证内容出错，请按照错误提示检查您的输入'
                    });
                } else {
                    $.ajax({
                        type: 'POST',
                        dataType: 'json',
                        url: '/api/library/news/',
                        cache: false,
                        data: {
                            official_account: $('#current-official-account').val(),
                            news_array: JSON.stringify(news_array)
                        },
                        beforeSend: function (xhr, settings) {
                            xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
                            that.$('#submit_news').attr('disabled', 'disabled');
                            that.$('#submit_news').text('提交中…');
                        },
                        success: function (data) {
                            noty({
                                type: "success",
                                text: "成功添加 <strong>" + data.news_array[0]['title'] + "</strong> 图文素材"
                            });
                            window.location.href = "#";
                        },
                        statusCode: {
                            400: function (xhr) {
                                var data = $.parseJSON(xhr.responseText);
                                var errors = {};
                                if (data.hasOwnProperty('news_array')) {
                                    for (var i = 0; i < data.news_array.length; i++) {
                                        if (!$.isEmptyObject(data.news_array[i])) {
                                            that._set_news_current(i);
                                            that._update_editor(i);
                                            that._set_editor_error_info(data.news_array[i]);
                                            break;
                                        }
                                    }
                                }
                            }
                        },
                        complete: function() {
                            that.$("#submit_news").removeAttr("disabled");
                            that.$("#submit_news").text("提交");
                        }
                    });
                }
            });
        }
    });

    var LibraryNewsItemEditView = Backbone.View.extend({
        template: _.template(edit_template),
        initialize: function (args) {
            this.news = new LibraryNewsModel({id: args.id});
            this.listenTo(this.news, 'change', this.render_library_news);

            localStorage.setItem('news_current', '0');
            localStorage.setItem('news_array', JSON.stringify([this._get_empty_news()]));
        },
        events: {
            "click #add_sub_news": "add_sub_news",
            "click .edit": "edit_sub_news",
            "click .delete": "delete_sub_news"
        },
        /**
         * 渲染添加图文素材页面
         * @returns {LibraryNewsItemAddView}
         */
        render: function () {
            this.$el.html(this.template());

            this.render_library_news(this.news);
            this.news.fetch({async: false});
            this.set_validate();

            return this;
        },
        /**
         * 当图文变动时渲染图文页面
         * @param news
         */
        render_library_news: function (news) {
            if (news.get('title')) {
                this.$('input:radio[name="pattern"]').on('change', this, this._trigger_pattern);

                var i;
                var multi_item = news.get('multi_item');
                var news_array = [];
                var news_current = 0;
                for (i = 0; i < multi_item.length; i++) {
                    news_array.push(this._get_empty_news());
                    news_array[i].title = multi_item[i].title || "";
                    news_array[i].description = multi_item[i].description || "";
                    news_array[i].picture = multi_item[i].picture || "";
                    news_array[i].author = multi_item[i].author || "";
                    if (multi_item[i].content) {
                        news_array[i].pattern = 'text';
                        news_array[i].content = multi_item[i].content || "";
                    } else {
                        news_array[i].pattern = 'url';
                        news_array[i].url = multi_item[i].content_url || "";
                    }
                    news_array[i].from_url = multi_item[i].from_url || "";
                }
                localStorage.setItem('news_current', news_current);
                localStorage.setItem('news_array', JSON.stringify(news_array));

                for (i = 1; i < news_array.length; i++) {  // 注意因为至少存在一条图文，默认图文已经在模板中写好，所以从 i=1 开始动态添加
                    this.$('.appmsg_content').append(_.template(add_sub_news_template)({'id': i}));
                    this._update_editor_title(i);
                    this._update_editor_picture(i);
                }
                this._update_editor(news_current);
            }
        },

        /**
         * 当点击添加子图文按钮时触发该函数
         */
        add_sub_news: function () {
            var news_array = this._get_news_array();
            var news_sum = news_array.length;

            if (news_sum >= 10) {
                noty({
                    type: "error",
                    text: "您最多只能添加十条图文"
                });
                return;
            }
            this.$('.appmsg_content').append(_.template(add_sub_news_template)({'id': news_sum}));
            news_array.push(this._get_empty_news());
            this._set_news_array(news_array);
        },
        /**
         * 当点击编辑子图文按钮时触发该函数
         * @param event
         */
        edit_sub_news: function (event) {
            var news_array = this._get_news_array();
            var news_id = parseInt($(event.currentTarget).attr('data-news-id'));

            this._set_news_current(news_id);
            this._update_editor(news_id);
        },
        /**
         * 当点击删除子图文按钮时触发该函数
         * @param event
         */
        delete_sub_news: function (event) {
            var news_array = this._get_news_array();
            var news_current = this._get_news_current();
            var news_id = parseInt($(event.currentTarget).attr('data-news-id'));
            this.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ')').remove();
            this._update_preview_area();
            news_array.splice(news_id, 1);
            if ((news_id == news_current && news_current >= news_array.length) || (news_id < news_current)) {
                news_current--;
            }
            this._set_news_array(news_array);
            this._set_news_current(news_current);
            this._update_editor(news_current);
        },
        /**
         * Hack: 修正首图文无法在渲染时获得事件绑定问题，由上层在HTML渲染好后负责调用
         */
        fix_ckeditor: function () {
            this._update_editor(this._get_news_current());
        },
        /**
         * 更新所有左侧预览图文中的序号 (用于对左侧预览图文顺序变动后)
         * @private
         */
        _update_preview_area: function () {
            this.$('.appmsg_content .js_appmsg_item').each(function (index) {
                $(this).find('.edit').attr('data-news-id', index);
                $(this).find('.delete').attr('data-news-id', index);
            });
        },
        /**
         * 更新编辑表单中的所有信息并且移动到适当位置
         * @param news_id {Number}
         * @private
         */
        _update_editor: function (news_id) {
            // 更新编辑框的位置
            if (news_id == 0) {
                this.$('#editor').css('margin-top', '0');
            } else {
                this.$('#editor').css('margin-top', 79 + news_id * 119 + 'px');
            }

            this._clear_editor_error_info();
            this._update_editor_title(news_id);
            this._update_editor_author(news_id);
            this._update_editor_picture(news_id);
            this._update_editor_description(news_id);
            this._update_editor_content(news_id);
            this._update_editor_url(news_id);
            this._update_editor_pattern(news_id);
            this._update_editor_from_url(news_id);
        },
        _update_editor_title: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('input[name="title"]').val(news_array[news_id].title);
            this.$('input[name="title"]').unbind('input propertychange change');
            this.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') .appmsg_title a').html(news_array[news_id].title || "标题");
            this.$('input[name="title"]').bind('input propertychange', function () {
                that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') .appmsg_title a').html($(this).val());
            });
            this.$('input[name="title"]').bind('change', function () {
                news_array = that._get_news_array();
                news_array[news_id].title = $(this).val();
                that._set_news_array(news_array);
            });
        },
        _update_editor_author: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('input[name="author"]').val(news_array[news_id].author);
            this.$('input[name="author"]').unbind('change');
            this.$('input[name="author"]').bind('change', function () {
                news_array = that._get_news_array();
                news_array[news_id].author = $(this).val();
                that._set_news_array(news_array);
            });
        },
        _update_editor_picture: function (news_id) {
            this.set_file_upload(news_id);
        },
        _update_editor_description: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('textarea[name="description"]').val(news_array[news_id].description);
            this.$('textarea[name="description"]').unbind('change');
            this.$('textarea[name="description"]').bind('change', function () {
                news_array = that._get_news_array();
                news_array[news_id].description = $(this).val();
                that._set_news_array(news_array);
            });
        },
        _update_editor_content: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('textarea[name="news_content"]').val(news_array[news_id].content);
            if (CKEDITOR.instances.hasOwnProperty('news_content')) {
                CKEDITOR.instances.news_content.setData(news_array[news_id].content);
            }
            if (CKEDITOR.instances.hasOwnProperty('news_content')) {
                var editor = CKEDITOR.instances.news_content;
                editor.on('change', function (event) {
                    var news_array = that._get_news_array();
                    var news_current = that._get_news_current();
                    news_array[news_current].content = editor.getData();
                    that._set_news_array(news_array);
                });
            }
        },
        _update_editor_url: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('input[name="url"]').val(news_array[news_id].url);
            this.$('input[name="url"]').unbind('change');
            this.$('input[name="url"]').bind('change', function () {
                news_array = that._get_news_array();
                news_array[news_id].url = $(this).val();
                that._set_news_array(news_array);
            });
        },
        _update_editor_pattern: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            if (news_array[news_id].pattern == 'text') {
                this.$('input:radio[name="pattern"][value="text"]').prop('checked', true).trigger('change');
            } else {
                this.$('input:radio[name="pattern"][value="url"]').prop('checked', true).trigger('change');
            }
        },
        _update_editor_from_url: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            this.$('input[name="from_url"]').val(news_array[news_id].from_url);
            this.$('input[name="from_url"]').unbind('change');
            this.$('input[name="from_url"]').bind('change', function () {
                news_array = that._get_news_array();
                news_array[news_id].from_url = $(this).val();
                that._set_news_array(news_array);
            });
        },
        /**
         * 设置编辑框的验证错误信息
         * @param data 验证错误信息
         * @private
         */
        _set_editor_error_info: function (data) {
            if (data.title) {
                this.$('#title_error').html(data.title[0]);
            }
            if (data.author) {
                this.$('#author_error').html(data.author[0]);
            }
            if (data.description) {
                this.$('#description_error').html(data.description[0]);
            }
            if (data.content) {
                this.$('#content_error').html(data.content[0]);
            }
            if (data.url) {
                this.$('#content_error').html(data.url[0]);
            }
            if (data.from_url) {
                this.$('#from_url_error').html(data.from_url[0]);
            }
        },
        /**
         * 清除编辑框的验证错误信息
         * @private
         */
        _clear_editor_error_info: function () {
            this.$('#title_error').html('');
            this.$('#author_error').html('');
            this.$('#description_error').html('');
            this.$('#content_error').html('');
            this.$('#from_url_error').html('');
        },
        /**
         * 触发内容展现方式 radio 时触发此函数
         * @param event
         * @private
         */
        _trigger_pattern: function (event) {
            var news_array = event.data._get_news_array();
            var news_current = event.data._get_news_current();
            if (event.data.$el.find('input[name="pattern"]:checked').val() === 'text') {
                event.data.$('#text_content').css('display', 'block');
                event.data.$('#url_content').css('display', 'none');
                news_array[news_current].pattern = 'text';
            } else {
                event.data.$('#text_content').css('display', 'none');
                event.data.$('#url_content').css('display', 'block');
                news_array[news_current].pattern = 'url';
            }
            news_array = event.data._set_news_array(news_array);
        },
        /**
         * 返回 localStorage 中存储的当前正在编辑的图文序号
         * @returns {Number}
         * @private
         */
        _get_news_current: function () {
            return parseInt(localStorage.getItem('news_current'));
        },
        /**
         * 设置 localStorage 中存储的当前正在编辑的图文序号
         * @param news_id {Number}
         * @private
         */
        _set_news_current: function (news_id) {
            localStorage.setItem('news_current', news_id);
        },
        /**
         * 返回 localStorage 中存储的当前图文信息数组
         * @returns {*}
         * @private
         */
        _get_news_array: function () {
            return JSON.parse(localStorage.getItem('news_array'));
        },
        /**
         * 设置 localStorage 中的当前图文信息数组
         * @param news {Array}
         * @private
         */
        _set_news_array: function (news) {
            localStorage.setItem('news_array', JSON.stringify(news));
        },
        /**
         * 生成一个空的 news 对象, 默认使用文本内容
         * @returns {{title: string, description: string, picture: string, author: string, pattern: string, content: string, url: string, from_url: string}}
         * @private
         */
        _get_empty_news: function () {
            return {
                title: '',
                description: '',
                picture: '',
                author: '',
                pattern: 'text',
                content: '',
                url: '',
                from_url: ''
            }
        },
        /**
         * 删除系统媒体文件
         * @param key 媒体文件标识符 key
         * @returns {*}
         */
        delete_media_file: function (key) {
            return $.ajax({
                url: '/api/filetranslator/' + key + '/',
                type: 'DELETE',
                async: false,
                error: function () {
                    noty({
                        type: "error",
                        text: "删除文件时出错, 请重试"
                    });
                }
            });
        },
        /**
         * 设置页面中的文件上传组件
         */
        set_file_upload: function (news_id) {
            var that = this;
            var news_array = this._get_news_array();
            var info = this.$('#upload_picture .upload-info');
            var progress = this.$('#upload_picture .upload-progress');
            var btn = this.$('#upload_picture .upload-button');

            info.set_content = function (url, key) {
                var content = '<div class="news-picture"><img class="img-responsive img-rounded" src="' + url + '" ></div>';
                content += '<div class="news-picture-opr"><strong><a class="delete-media" data-key="' + key + '" href="javascript:void(0)">删除该文件</a></strong></div>';
                content += '<div class="clearfix"></div>';
                $(this).html(content);
                $(this).find('.delete-media').click(function () {
                    var key = $(this).attr('data-key');
                    that.delete_media_file(key).success(function () {
                        btn.display_select_upload();
                        info.hide();
                        news_array[news_id].picture = '';
                        that._set_news_array(news_array);

                        // 当删除首图文图片时的同时恢复左侧预览图为默认图片
                        if (news_id == 0) {
                            that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb_wrp img').attr('src', '');
                            that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb').css('display', 'block');
                            that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb_wrp img').css('display', 'none');
                        } else {
                            that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') img').attr('src', '');
                            that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') .appmsg_thumb').css('display', 'block');
                            that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') img').css('display', 'none');
                        }
                    });
                });

                // 当上传图片成功时设置左侧预览图为对应图片
                if (news_id == 0) {
                    that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb_wrp img').attr('src', url);
                    that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb').css('display', 'none');
                    that.$('.appmsg_content .js_appmsg_item:nth-child(1) .appmsg_thumb_wrp img').css('display', 'block');
                } else {
                    that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') img').attr('src', url);
                    that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') .appmsg_thumb').css('display', 'none');
                    that.$('.appmsg_content .js_appmsg_item:nth-child(' + (news_id+1) + ') img').css('display', 'block');
                }
            };
            info.set_error_content = function (content) {
                $(this).html('<span class="text-red">上传失败：' + content + '</span>');
            };
            progress.set_progress = function (percent) {
                progress.find('.progress-bar').css('width', percent + '%');
                progress.find('.progress-bar').attr('aria-valuenow', percent);
                progress.find('.progress-bar').html(percent + '%');
            };
            btn.display_select_upload = function () {
                $(this).find('input').prop('disabled', false);
                $(this).removeClass('disabled');
                $(this).find('span').html('上传');
            };
            btn.display_uploading = function () {
                $(this).find('input').prop('disabled', true);
                $(this).addClass('disabled');
                $(this).find('span').html('上传中...');
            };
            btn.display_restart_upload = function () {
                $(this).find('input').prop('disabled', false);
                $(this).removeClass('disabled');
                $(this).find('span').html('重新上传');
            };

            this.$('input[id="picture"]').unbind('click change');
            if (news_array[news_id].picture.length > 0) {  // 当该子图文已经上传过封面图片时，直接请求并显示，否则重建上传框
                btn.display_restart_upload();
                progress.hide();
                $.ajax({
                    url: '/api/filetranslator/' + news_array[news_id].picture + '/',
                    type: 'GET',
                    dataType: 'json',
                    async: false,
                    success: function (data) {
                        info.set_content(data['url'], data['key']);
                        info.show();
                    }
                });
            } else {
                info.hide();
                progress.set_progress(0);
                progress.hide();
                btn.display_select_upload();
            }

            this.$('input[id="picture"]').click(function () {  // 此处为两次提交重复文件不响应 change 的解决方案
                $(this).val('');
            });
            this.$('input[id="picture"]').change(function () {
                var news_array = that._get_news_array();
                that.$('#upload_picture form').ajaxSubmit({
                    dataType: 'json',
                    data: {
                        'official_account': $('#current-official-account').val(),
                        'type': 1
                    },
                    beforeSend: function (xhr) {
                        var origin_key = news_array[news_id].picture;
                        if (origin_key.length > 0) {  // 当原先存在封面图片时先删除原先的
                            that.delete_media_file(origin_key).success(function () {
                                news_array[news_id].picture = '';
                                that._set_news_array(news_array);
                            });
                        }

                        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                        btn.display_uploading();
                        progress.set_progress(0);
                        progress.show();
                        info.hide();
                    },
                    uploadProgress: function (event, position, total, percentComplete) {
                        progress.set_progress(percentComplete);
                    },
                    success: function (data) {
                        news_array[news_id].picture = data['key'];
                        that._set_news_array(news_array);

                        btn.display_restart_upload();
                        progress.hide();
                        info.set_content(data['url'], data['key']);
                        info.show();
                    },
                    statusCode: {
                        400: function(xhr) {
                            var data = $.parseJSON(xhr.responseText);
                            for (var key in data) {
                                btn.display_select_upload();
                                progress.hide();
                                info.set_error_content(data[key][0]);
                                info.show();
                                break;  // 直接针对第一条错误给出提示, 其他忽略
                            }
                        },
                        500: function(xhr) {
                            btn.display_select_upload();
                            progress.hide();
                            info.hide();
                            noty({
                                type: "error",
                                text: "服务器内部出错, 请重试"
                            });
                        }
                    },
                    error: function(xhr) {
                        if (xhr.status != 400 && xhr.status != 500) {
                            btn.display_select_upload();
                            progress.hide();
                            if (xhr.status == 413) {
                                info.set_error_content('错误' + xhr.status + ' - 请求数据过长，请尝试增大服务器最大上传限制');
                            } else {
                                info.set_error_content('错误' + xhr.status);
                            }
                            info.show();
                        }
                    }
                });
            });
        },
        /**
         * 设置表单的验证
         */
        set_validate: function() {
            var that = this;
            this.$('#submit_news').bind('click', function () {
                that._clear_editor_error_info();

                var news_array = that._get_news_array();
                var news_current = that._get_news_current();
                var error = {};
                var error_flag = false;

                for (var i = 0; i < news_array.length; i++) {
                    error.current_position = i;
                    if (news_array[i].title.length == 0) {
                        error.title = ['图文标题不能为空'];
                        error_flag = true;
                    } else if (news_array[i].title.length > 100) {
                        error.title = ['图文标题最长为 100 字符'];
                        error_flag = true;
                    }

                    if (news_array[i].author.length > 100) {
                        error.author = ['作者最长为 100 字符'];
                        error_flag = true;
                    }

                    if (news_array[i].pattern == 'text' && news_array[i].content == 0) {
                        error.content = ['图文内容不能为空'];
                        error_flag = true;
                    } else if (news_array[i].pattern == 'url' && news_array[i].url == 0) {
                        error.url = ['跳转链接不能为空'];
                        error_flag = true;
                    }

                    if (error_flag) {
                        break;
                    }
                }

                if (error_flag) {
                    that._set_news_current(error.current_position);
                    that._update_editor(error.current_position);
                    that._set_editor_error_info(error);
                    noty({
                        type: 'error',
                        text: '验证内容出错，请按照错误提示检查您的输入'
                    });
                } else {
                    $.ajax({
                        type: 'PUT',
                        dataType: 'json',
                        url: '/api/library/news/' + that.news.get('id') + '/',
                        cache: false,
                        data: {
                            official_account: $('#current-official-account').val(),
                            news_array: JSON.stringify(news_array)
                        },
                        beforeSend: function (xhr, settings) {
                            xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
                            that.$('#submit_news').attr('disabled', 'disabled');
                            that.$('#submit_news').text('提交中…');
                        },
                        success: function (data) {
                            noty({
                                type: "success",
                                text: "成功修改 <strong>" + data.news_array[0]['title'] + "</strong> 图文素材"
                            });
                            window.location.href = "#";
                        },
                        statusCode: {
                            400: function (xhr) {
                                var data = $.parseJSON(xhr.responseText);
                                var errors = {};
                                if (data.hasOwnProperty('news_array')) {
                                    for (var i = 0; i < data.news_array.length; i++) {
                                        if (!$.isEmptyObject(data.news_array[i])) {
                                            that._set_news_current(i);
                                            that._update_editor(i);
                                            that._set_editor_error_info(data.news_array[i]);
                                            break;
                                        }
                                    }
                                }
                            }
                        },
                        complete: function() {
                            that.$("#submit_news").removeAttr("disabled");
                            that.$("#submit_news").text("提交");
                        }
                    });
                }
            });
        }
    });

    module.exports = {
        'LibraryNewsModel': LibraryNewsModel,
        'LibraryNewsCollection': LibraryNewsCollection,
        'LibraryNewsItemView': LibraryNewsItemView,
        'LibraryNewsListView': LibraryNewsListView,
        'LibraryNewsItemAddView': LibraryNewsItemAddView,
        'LibraryNewsItemEditView': LibraryNewsItemEditView
    }
});