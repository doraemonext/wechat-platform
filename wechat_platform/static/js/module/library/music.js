define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var ConfirmModal = require('helper.confirm-modal');
    require('spin');
    require('jquery-validate');
    require('jquery-cookie');
    require('jquery-form');
    require('backbone-paginator');

    var item_template = require('text!templates/library/music/item.html');
    var list_template = require('text!templates/library/music/list.html');
    //var detail_template = require('text!templates/library/music/detail.html');
    var add_template = require('text!templates/library/music/edit.html');
    var edit_template = require('text!templates/library/music/edit.html');

    var confirm_modal_view = new ConfirmModal;

    var MediaModel = Backbone.Model.extend({
        urlRoot: '/api/filetranslator/'
    });
    var LibraryMusicModel = Backbone.Model.extend({
        urlRoot: '/api/library/music/'
    });
    var LibraryMusicCollection = Backbone.PageableCollection.extend({
        url: '/api/library/music/?official_account=' + $('#current-official-account').val(),
        model: LibraryMusicModel,
        state: {
            pageSize: 15
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
        render: function () {
            this.$el.html(this.template());
            this.set_file_upload('music');
            this.set_file_upload('hq_music');
            this.set_file_upload('thumb');
            this.set_validate();
            return this;
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
         * @param media_type 组件标识符 (可选 music/hq_music/thumb)
         */
        set_file_upload: function (media_type) {
            var that = this;
            var info = this.$('#upload_' + media_type + ' .upload-info');
            var progress = this.$('#upload_' + media_type + ' .upload-progress');
            var btn = this.$('#upload_' + media_type + ' .upload-button');

            info.set_content = function (filename, size, key) {
                var content = '<strong>文件名</strong>: ' + filename + ' <strong>大小</strong>: ' + size + ' KB ';
                content += '&nbsp;<strong><a class="delete-media" data-key="' + key +'" href="javascript:void(0)">删除该文件</a></strong>';
                $(this).html(content);
                $(this).find('.delete-media').click(function () {
                    var key = $(this).data('key');
                    that.delete_media_file(key).success(function () {
                        btn.display_select_upload();
                        info.hide();
                        that.$('input[name=' + media_type + ']').val('');
                    });
                });
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
                $(this).find('span').html('上传文件');
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

            this.$('input[id=' + media_type + '_media]').click(function () {  // 此处为两次提交重复文件不响应 change 的解决方案
                $(this).val('');
            });
            this.$('input[id=' + media_type + '_media]').change(function () {
                var media_type_number;
                if (media_type == 'music' || media_type == 'hq_music') {
                    media_type_number = 3;
                } else {
                    media_type_number = 1;
                }
                that.$('#upload_' + media_type + ' form').ajaxSubmit({
                    dataType: 'json',
                    data: {
                        'official_account': $('#current-official-account').val(),
                        'type': media_type_number
                    },
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));

                        var origin_key = that.$('input[name=' + media_type + ']').val();
                        if (origin_key.length > 0) {
                            that.delete_media_file(origin_key);
                        }
                        btn.display_uploading();
                        progress.set_progress(0);
                        progress.show();
                        info.hide();
                    },
                    uploadProgress: function (event, position, total, percentComplete) {
                        progress.set_progress(percentComplete);
                    },
                    success: function (data) {
                        that.$('input[name=' + media_type + ']').val(data['key']);

                        var full_filename = data['filename'] + data['extension'];
                        var size = parseInt(parseInt(data['size']) / 1024);

                        btn.display_restart_upload();
                        progress.hide();
                        info.set_content(full_filename, size, data['key']);
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
                        if (xhr.status != 400 && xhr.status != 400) {
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
            this.$('#form').validate({
                errorClass: 'control-label text-red',
                errorPlacement: function(error, element) {
                    if ($(element).prop('name') == 'music') {
                        that.$('#upload_music .upload-info').html('<span class="text-red">' + error.html() + '</span>');
                        that.$('#upload_music .upload-info').show();
                    } else if ($(element).prop('name') == 'hq_music') {
                        that.$('#upload_hq_music .upload-info').html('<span class="text-red">' + error.html() + '</span>');
                        that.$('#upload_hq_music .upload-info').show();
                    } else if ($(element).prop('name') == 'thumb') {
                        that.$('#upload_thumb .upload-info').html('<span class="text-red">' + error.html() + '</span>');
                        that.$('#upload_thumb .upload-info').show();
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
                        url: '/api/library/music/',
                        cache: false,
                        data: {
                            official_account: $('#current-official-account').val(),
                            plugin_iden: 'music',
                            title: that.$('input[name=title]').val(),
                            description: that.$('textarea[name=description]').val(),
                            music: that.$('input[name=music]').val(),
                            hq_music: that.$('input[name=hq_music]').val(),
                            thumb: that.$('input[name=thumb]').val()
                        },
                        beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                            that.$("button[type=submit]").attr("disabled", "disabled");
                            that.$("button[type=submit]").text("提交中…");
                        },
                        success: function(data) {
                            noty({
                                type: "success",
                                text: "成功添加 <strong>" + data["title"] + "</strong> 音乐素材"
                            });
                            window.location.href = "#";
                        },
                        statusCode: {
                            400: function(xhr) {
                                var data = $.parseJSON(xhr.responseText);
                                var errors = {};
                                for (var key in data) {
                                    if (key == "non_field_errors") {
                                        errors["title"] = data[key][0];
                                    } else {
                                        errors[key] = data[key][0];
                                    }
                                }
                                validator.showErrors(errors);
                            }
                        },
                        complete: function() {
                            that.$("button[type=submit]").removeAttr("disabled");
                            that.$("button[type=submit]").text("提交");
                        }
                    });
                    return false;
                }
            });
        }
    });

    var LibraryMusicItemEditView = Backbone.View.extend({
        template: _.template(edit_template),
        initialize: function (args) {
            this.music = new LibraryMusicModel({id: args.id});
            this.listenTo(this.music, 'change', this.render_library_music);
        },
        /**
         * 渲染编辑音乐素材页面
         * @returns {LibraryMusicItemEditView}
         */
        render: function () {
            this.$el.html(this.template());

            this.render_library_music(this.music);
            this.music.fetch();
            this.set_validate();

            return this;
        },
        render_library_music: function (music) {
            if (music.get('music')) {
                this.$('input[name=music]').val(music.get('music'));
                this.$('input[name=hq_music]').val(music.get('hq_music'));
                this.$('input[name=thumb]').val(music.get('thumb'));
                this.$('input[name=title]').val(music.get('title'));
                this.$('textarea[name=description]').val(music.get('description'));
                this.set_file_upload('music');
                this.set_file_upload('hq_music');
                this.set_file_upload('thumb');
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
         * @param media_type 组件标识符 (可选 music/hq_music/thumb)
         */
        set_file_upload: function (media_type) {
            var that = this;
            var info = this.$('#upload_' + media_type + ' .upload-info');
            var progress = this.$('#upload_' + media_type + ' .upload-progress');
            var btn = this.$('#upload_' + media_type + ' .upload-button');

            info.set_content = function (filename, size, key) {
                var content = '<strong>文件名</strong>: ' + filename + ' <strong>大小</strong>: ' + size + ' KB ';
                content += '&nbsp;<strong><a class="delete-media" data-key="' + key +'" href="javascript:void(0)">删除该文件</a></strong>';
                $(this).html(content);
                $(this).find('.delete-media').click(function () {
                    var key = $(this).data('key');
                    that.delete_media_file(key).success(function () {
                        btn.display_select_upload();
                        info.hide();
                        that.$('input[name=' + media_type + ']').val('');
                    });
                });
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
                $(this).find('span').html('上传文件');
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

            if (this.music.get(media_type)) {
                var media = new MediaModel({id: this.music.get(media_type)});
                media.fetch({
                    success: function(model) {
                        var full_filename = model.get('filename') + model.get('extension');
                        var size = parseInt(parseInt(model.get('size')) / 1024);
                        info.set_content(full_filename, size, that.music.get(media_type));
                        info.show();
                        progress.hide();
                        btn.display_restart_upload();
                    }
                })
            }

            this.$('input[id=' + media_type + '_media]').click(function () {  // 此处为两次提交重复文件不响应 change 的解决方案
                $(this).val('');
            });
            this.$('input[id=' + media_type + '_media]').change(function () {
                var media_type_number;
                if (media_type == 'music' || media_type == 'hq_music') {
                    media_type_number = 3;
                } else {
                    media_type_number = 1;
                }
                that.$('#upload_' + media_type + ' form').ajaxSubmit({
                    dataType: 'json',
                    data: {
                        'official_account': $('#current-official-account').val(),
                        'type': media_type_number
                    },
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));

                        var origin_key = that.$('input[name=' + media_type + ']').val();
                        if (origin_key.length > 0) {
                            that.delete_media_file(origin_key);
                        }
                        btn.display_uploading();
                        progress.set_progress(0);
                        progress.show();
                        info.hide();
                    },
                    uploadProgress: function (event, position, total, percentComplete) {
                        progress.set_progress(percentComplete);
                    },
                    success: function (data) {
                        that.$('input[name=' + media_type + ']').val(data['key']);

                        var full_filename = data['filename'] + data['extension'];
                        var size = parseInt(parseInt(data['size']) / 1024);

                        btn.display_restart_upload();
                        progress.hide();
                        info.set_content(full_filename, size, data['key']);
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
                        if (xhr.status != 400 && xhr.status != 400) {
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
            this.$('#form').validate({
                errorClass: 'control-label text-red',
                errorPlacement: function(error, element) {
                    if ($(element).prop('name') == 'music') {
                        that.$('#upload_music .upload-info').html('<span class="text-red">' + error.html() + '</span>');
                        that.$('#upload_music .upload-info').show();
                    } else if ($(element).prop('name') == 'hq_music') {
                        that.$('#upload_hq_music .upload-info').html('<span class="text-red">' + error.html() + '</span>');
                        that.$('#upload_hq_music .upload-info').show();
                    } else if ($(element).prop('name') == 'thumb') {
                        that.$('#upload_thumb .upload-info').html('<span class="text-red">' + error.html() + '</span>');
                        that.$('#upload_thumb .upload-info').show();
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
                        url: '/api/library/music/' + that.music.get('id') + '/',
                        cache: false,
                        data: {
                            official_account: $('#current-official-account').val(),
                            plugin_iden: 'music',
                            title: that.$('input[name=title]').val(),
                            description: that.$('textarea[name=description]').val(),
                            music: that.$('input[name=music]').val(),
                            hq_music: that.$('input[name=hq_music]').val(),
                            thumb: that.$('input[name=thumb]').val()
                        },
                        beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                            that.$("button[type=submit]").attr("disabled", "disabled");
                            that.$("button[type=submit]").text("提交中…");
                        },
                        success: function(data) {
                            noty({
                                type: "success",
                                text: "成功编辑 <strong>" + data["title"] + "</strong> 音乐素材"
                            });
                            window.location.href = "#";
                        },
                        statusCode: {
                            400: function(xhr) {
                                var data = $.parseJSON(xhr.responseText);
                                var errors = {};
                                for (var key in data) {
                                    if (key == "non_field_errors") {
                                        errors["title"] = data[key][0];
                                    } else {
                                        errors[key] = data[key][0];
                                    }
                                }
                                validator.showErrors(errors);
                            }
                        },
                        complete: function() {
                            that.$("button[type=submit]").removeAttr("disabled");
                            that.$("button[type=submit]").text("提交");
                        }
                    });
                    return false;
                }
            });
        }
    });

    module.exports = {
        'LibraryMusicModel': LibraryMusicModel,
        'LibraryMusicCollection': LibraryMusicCollection,
        'LibraryMusicItemView': LibraryMusicItemView,
        'LibraryMusicListView': LibraryMusicListView,
        'LibraryMusicItemAddView': LibraryMusicItemAddView,
        'LibraryMusicItemEditView': LibraryMusicItemEditView
    }
});