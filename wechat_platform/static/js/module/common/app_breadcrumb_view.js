define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var app_breadcrumb_template = require('text!templates/common/app_breadcrumb.html');

    var BreadcrumbView = Backbone.View.extend({
        tagName: "section",
        className: "content-header",
        template: _.template(app_breadcrumb_template),
        initialize: function(args) {
            this.title = args.title;
            this.subtitle = args.subtitle;
            this.breadcrumbs = args.breadcrumbs;
        },
        render: function() {
            this.$el.html(this.template({
                title: this.title,
                subtitle: this.subtitle,
                breadcrumbs: this.breadcrumbs
            }));
            return this;
        }
    });

    return BreadcrumbView;
});