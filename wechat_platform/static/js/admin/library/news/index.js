define(function (require, exports, module) {
    require('common');
    var $ = require('jquery');
    var Backbone = require('backbone');
    var CKEDITOR = require('ckeditor');

    var CommonAppView = require('module.common.app-view');
    var BreadcrumbView = require('module.common.app-breadcrumb-view');
    var ContentHeaderView = require('module.common.app-content-header-view');

    var LibraryNewsModule = require('module.library.news');
    var LibraryNewsModel = LibraryNewsModule.LibraryNewsModel;
    var LibraryNewsCollection = LibraryNewsModel.LibraryNewsCollection;
    var LibraryNewsItemView = LibraryNewsModule.LibraryNewsItemView;
    var LibraryNewsListView = LibraryNewsModule.LibraryNewsListView;
    var LibraryNewsItemAddView = LibraryNewsModule.LibraryNewsItemAddView;
//    var LibraryMusicItemEditView = LibraryMusicModule.LibraryMusicItemEditView;

    var AppView = CommonAppView.extend({
        default_interface: function () {
            this.set_breadcrumb(new BreadcrumbView({
                title: '图文素材',
                subtitle: '管理本地素材库中的图文消息',
                breadcrumbs: [
                    { title: '素材管理', url: '#' },
                    { title: '图文素材', url: '#' }
                ]
            }));
            this.set_header(new ContentHeaderView({
                html: require('text!templates/library/news/app_content_header_list.html')
            }));
            this.set_content(new LibraryNewsListView);
        },
        add_interface: function () {
            this.set_breadcrumb(new BreadcrumbView({
                title: '添加图文素材',
                subtitle: '在本地素材库中添加新的图文素材',
                breadcrumbs: [
                    { title: '素材管理', url: '#' },
                    { title: '图文素材', url: '#' },
                    { title: '添加图文素材', url: '#' }
                ]
            }));
            this.set_header(new ContentHeaderView({
                html: require('text!templates/library/news/app_content_header_add.html')
            }));
            this.set_content(new LibraryNewsItemAddView);
            CKEDITOR.replace('news_content', {
                language: 'zh-cn'
            });
        },
//        edit_interface: function (id) {
//            this.set_breadcrumb(new BreadcrumbView({
//                title: '编辑音乐素材',
//                subtitle: '编辑该音乐素材的详细信息',
//                breadcrumbs: [
//                    { title: '素材管理', url: '#' },
//                    { title: '音乐素材', url: '#' },
//                    { title: '编辑音乐素材', url: '#/edit/' + id }
//                ]
//            }));
//            this.set_header(new ContentHeaderView({
//                html: require('text!templates/library/music/app_content_header_edit.html')
//            }));
//            this.set_content(new LibraryMusicItemEditView({
//                id: id
//            }));
//        }
    });
    var app_view = new AppView;

    var AppRouter = Backbone.Router.extend({
        routes: {
            'add': 'add',
//            'edit/:id': 'edit',
//            'detail/:id': 'detail',
            '*actions': 'default_router'
        },
        add: function () {
            app_view.add_interface();
        },
//        edit: function (id) {
//            app_view.edit_interface(id);
//        },
        default_router: function (actions) {
            app_view.default_interface();
        }
    });
    var app_router = new AppRouter;
    Backbone.history.start();
});
