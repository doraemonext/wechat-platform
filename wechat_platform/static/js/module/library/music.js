define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var ConfirmModal = require('helper.confirm-modal');
    require('jquery-validate');
    require('jquery-cookie');
    require('backbone-paginator');

    var item_template = require('text!templates/library/music/item.html');
    var list_template = require('text!templates/library/music/list.html');
    //var detail_template = require('text!templates/library/music/detail.html');
    //var add_template = require('text!templates/library/music/edit.html');
    //var edit_template = require('text!templates/library/music/edit.html');

    var confirm_modal_view = new ConfirmModal;

    var LibraryMusicModel = Backbone.Model.extend({
        urlRoot: '/api/library/music/'
    });
    var LibraryMusicCollection = Backbone.PageableCollection.extend({
        url: '/api/library/music/',
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
            "click .pagination-next": "pagination_next"
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

    module.exports = {
        'LibraryMusicModel': LibraryMusicModel,
        'LibraryMusicCollection': LibraryMusicCollection,
        'LibraryMusicListView': LibraryMusicListView
    }
});