define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var ConfirmModal = require('helper.confirm-modal');
    require('jquery-validate');
    require('jquery-cookie');

    //var item_template = require('text!templates/library/music/item.html');
    var list_template = require('text!templates/library/music/list.html');
    //var detail_template = require('text!templates/library/music/detail.html');
    //var add_template = require('text!templates/library/music/edit.html');
    //var edit_template = require('text!templates/library/music/edit.html');

    var confirm_modal_view = new ConfirmModal;

    var LibraryMusicModel = Backbone.Model.extend({
        urlRoot: '/api/library/music/'
    });
    var LibraryMusicCollection = Backbone.Collection.extend({
        url: '/api/library/music/',
        model: LibraryMusicModel
    });

    var LibraryMusicListView = Backbone.View.extend({
        template: _.template(list_template),
        initialize: function() {
            this.collection = new LibraryMusicCollection;
//            this.listenTo(this.collection, 'add', this.add);
        },
        render: function() {
            this.$el.html(this.template());
//            var that = this;
//            this.$el.html(this.template());
//            _(this.collection.models).each(this.add, this);
//            this.collection.fetch({
//                success: function(collection) {
//                    if (!collection.length) {
//                        that.$('#no-official-account').css('display', 'block');
//                    }
//                }
//            });
            return this;
        }
//        add: function(official_account) {
//            var official_account_view = new OfficialAccountItemView({model: official_account});
//            this.$('#no-official-account').css('display', 'none');
//            this.$(".list").append(official_account_view.render().el);
//        }
    });

    module.exports = {
        'LibraryMusicModel': LibraryMusicModel,
        'LibraryMusicCollection': LibraryMusicCollection,
        'LibraryMusicListView': LibraryMusicListView,
    }
});