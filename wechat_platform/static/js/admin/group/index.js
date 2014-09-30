define(function(require, exports, module) {
    require('common');
    var $ = require('jquery');
    var Backbone = require('backbone');

    var CommonAppView = require('module.common.app-view');
    var BreadcrumbView = require('module.common.app-breadcrumb-view');
    var ContentHeaderView = require('module.common.app-content-header-view');

    var GroupModule = require('module.group');
    var GroupItemDetailView = GroupModule.GroupItemDetailView;
    var GroupListView = GroupModule.GroupListView;
    var GroupItemAddView = GroupModule.GroupItemAddView;
    var GroupItemEditView = GroupModule.GroupItemEditView;

    var AppView = CommonAppView.extend({
        default_interface: function() {
            this.set_breadcrumb(new BreadcrumbView({
                title: '用户组',
                subtitle: '管理当前系统中的用户组',
                breadcrumbs: [{title:'用户组', url:'#'}]
            }));
            this.set_header(new ContentHeaderView({
                html: require('text!templates/group/app_content_header_list.html')
            }));
            this.set_content(new GroupListView);
        },
        add_interface: function() {
            this.set_breadcrumb(new BreadcrumbView({
                title: '添加用户组',
                subtitle: '添加一个新的用户组',
                breadcrumbs: [{title:'用户组', url:'#'}, {title:'添加用户组', url:'#/add'}]
            }));
            this.set_header(new ContentHeaderView({
                html: require('text!templates/group/app_content_header_add.html')
            }));
            this.set_content(new GroupItemAddView);
        },
        edit_interface: function(id) {
            this.set_breadcrumb(new BreadcrumbView({
                title: '编辑用户组',
                subtitle: '编辑该用户组的详细信息',
                breadcrumbs: [{title:'用户组', url:'#'}, {title:'编辑用户组', url:'#/edit/'+id}]
            }));
            this.set_header(new ContentHeaderView({
                html: require('text!templates/group/app_content_header_edit.html')
            }));
            this.set_content(new GroupItemEditView({
                id: id
            }));
        },
        detail_interface: function(id) {
            this.set_breadcrumb(new BreadcrumbView({
                title: '用户组详情',
                subtitle: '查看用户组详细信息',
                breadcrumbs: [{title:'用户组', url:'#'}, {title:'用户组详情', url:'#/detail/'+id}]
            }));
            this.set_header(new ContentHeaderView({
                html: require('text!templates/group/app_content_header_detail.html'),
                data: {id: id}
            }));
            this.set_content(new GroupItemDetailView({id: id}));
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
