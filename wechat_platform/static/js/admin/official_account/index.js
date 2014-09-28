define(function(require, exports, module) {
    require('common');
    var $ = require('jquery');
    var Backbone = require('backbone');

    var CommonAppView = require('module.common.app-view');
    var BreadcrumbView = require('module.common.app-breadcrumb-view');
    var ContentHeaderView = require('module.common.app-content-header-view');

    var OfficialAccountModule = require('module.official-account');
    var OfficialAccount = OfficialAccountModule.OfficialAccount;
    var OfficialAccounts = OfficialAccountModule.OfficialAccounts;
    var OfficialAccountItemView = OfficialAccountModule.OfficialAccountItemView;
    var OfficialAccountItemDetailView = OfficialAccountModule.OfficialAccountItemDetailView;
    var OfficialAccountListView = OfficialAccountModule.OfficialAccountListView;

    var AppView = CommonAppView.extend({
        default_interface: function() {
            this.set_breadcrumb(new BreadcrumbView({
                title: '公众号管理',
                subtitle: '管理当前系统中的公众号',
                breadcrumbs: [{title:'公众号管理', url:'#'}]
            }));
            this.set_header(new ContentHeaderView({
                html: require('text!templates/official_account/app_content_header_list.html')
            }));
            this.set_content(new OfficialAccountListView);
        },
        add_interface: function() {
            this.set_breadcrumb(new BreadcrumbView({
                title: '添加公众号',
                subtitle: '添加一个新的公众号',
                breadcrumbs: [{title:'公众号管理', url:'#'}, {title:'添加公众号', url:'#/add'}]
            }));
            this.set_header(new ContentHeaderView({
                html: require('text!templates/official_account/app_content_header_add.html')
            }));
        },
        edit_interface: function(id) {
            this.set_breadcrumb(new BreadcrumbView({
                title: '编辑公众号',
                subtitle: '编辑该公众号的详细信息',
                breadcrumbs: [{title:'公众号管理', url:'#'}, {title:'编辑公众号', url:'#/edit/'+id}]
            }));
            this.set_header(new ContentHeaderView({
                html: require('text!templates/official_account/app_content_header_edit.html')
            }));
        },
        detail_interface: function(id) {
            this.set_breadcrumb(new BreadcrumbView({
                title: '公众号详情',
                subtitle: '查看公众号详细信息',
                breadcrumbs: [{title:'公众号管理', url:'#'}, {title:'公众号详情', url:'#/detail/'+id}]
            }));
            this.set_header(new ContentHeaderView({
                html: require('text!templates/official_account/app_content_header_detail.html'),
                data: {id: id}
            }));
            this.set_content(new OfficialAccountItemDetailView({id: id}));
        }
    });
    var app_view = new AppView;

    var AppRouter = Backbone.Router.extend({
        routes: {
            'add': 'add',
            'edit/:id': 'edit',
            'detail/:id': 'detail',
            '*actions': 'default_router'
        },
        add: function() {
            app_view.add_interface();
        },
        edit: function(id) {
            app_view.edit_interface(id);
        },
        detail: function(id) {
            app_view.detail_interface(id);
        },
        default_router: function(actions) {
            app_view.default_interface();
        }
    });
    var app_router = new AppRouter;
    Backbone.history.start();
});
