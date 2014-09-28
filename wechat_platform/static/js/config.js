require.config({
    baseUrl: '/static/js',
    shim: {
        'underscore': { 'exports': '_' },
        'bootstrap': { 'deps': ['jquery'] },
        'jquery-cookie': { 'deps': ['jquery'] },
        'noty': { 'deps': ['jquery'] },
        'jquery-validate': { 'deps': ['jquery'] }
    },
    paths: {
        'jquery': 'plugins/jquery/jquery.min',
        'underscore': 'plugins/underscore/underscore.min',
        'backbone': 'plugins/backbone/backbone.min',

        'bootstrap': 'plugins/bootstrap/bootstrap.min',
        'jquery-cookie': 'plugins/jquerycookie/jquery.cookie',
        'jquery-validate': 'plugins/jqueryvalidate/jquery.validate.min',
        'noty': 'plugins/noty/jquery.noty.packaged.min',
        'theme-app': 'AdminLTE/app',
        'common': 'common',

        'module.common.app-view': 'module/common/app_view',
        'module.common.app-breadcrumb-view': 'module/common/app_breadcrumb_view',
        'module.common.app-content-header-view': 'module/common/app_content_header_view',
        'module.official-account': 'module/official_account',

        'helper.confirm-modal': 'helper/confirm_modal/confirm_modal'
    }
});