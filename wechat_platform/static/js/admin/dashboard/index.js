define(function (require, exports, module) {
    require('common');
    var $ = require('jquery');
    var Backbone = require('backbone');

    var CommonAppView = require('module.common.app-view');
    var BreadcrumbView = require('module.common.app-breadcrumb-view');
    var ContentHeaderView = require('module.common.app-content-header-view');

    var AppView = CommonAppView.extend({
        default_interface: function () {
            this.set_breadcrumb(new BreadcrumbView({
                title: '仪表盘',
                subtitle: '显示当前系统信息',
                breadcrumbs: [
                    { title: '仪表盘', url: '#' }
                ]
            }));
        }
    });
    var app_view = new AppView;

    var AppRouter = Backbone.Router.extend({
        routes: {
            '*actions': 'default_router'
        },
        default_router: function (actions) {
            app_view.default_interface();
        }
    });
    var app_router = new AppRouter;
    Backbone.history.start();
});