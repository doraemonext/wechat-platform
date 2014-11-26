require.config({
    baseUrl: '/static/js',
    shim: {
        'underscore': { 'exports': '_' },
        'backbone-paginator': { 'deps': ['backbone'] },
        'bootstrap': { 'deps': ['jquery'] },
        'jquery-cookie': { 'deps': ['jquery'] },
        'noty': { 'deps': ['jquery'] },
        'jquery-validate': { 'deps': ['jquery'] },
        'jquery-form': { 'deps': ['jquery'] },
        'masonry': { 'deps': ['jquery'], 'exports': 'jQuery.masonry' },
        'spin': { 'exports': 'Spinner' },
        'theme-app': { 'deps': ['jquery', 'bootstrap'] }
    },
    paths: {
        'jquery': 'plugins/jquery/jquery.min',
        'underscore': 'plugins/underscore/underscore.min',
        'backbone': 'plugins/backbone/backbone.min',

        'backbone-paginator': 'plugins/backbone/backbone.paginator.min',
        'bootstrap': 'plugins/bootstrap/bootstrap.min',
        'jquery-cookie': 'plugins/jquerycookie/jquery.cookie',
        'jquery-validate': 'plugins/jqueryvalidate/jquery.validate.min',
        'jquery-form': 'plugins/jqueryform/jquery.form',
        'masonry': 'plugins/masonry/masonry.pkgd.min',
        'noty': 'plugins/noty/jquery.noty.packaged.min',
        'spin': 'plugins/spin/spin.min',
        'theme-app': 'AdminLTE/app',
        'common': 'common',

        'module.common.app-view': 'module/common/app_view',
        'module.common.app-breadcrumb-view': 'module/common/app_breadcrumb_view',
        'module.common.app-content-header-view': 'module/common/app_content_header_view',
        'module.official-account': 'module/official_account',
        'module.library.music': 'module/library/music',
        'module.library.news': 'module/library/news',

        'helper.confirm-modal': 'helper/confirm_modal/confirm_modal'
    }
});