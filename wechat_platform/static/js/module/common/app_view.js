define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');
    var app_template = require('text!templates/common/app.html');

    var AppView = Backbone.View.extend({
        el: $("#container"),
        template: _.template(app_template),
        initialize: function() {
            this.render();
            this.breadcrumb = this.$el.find(".right-side");
            this.header = this.$el.find("#header");
            this.content = this.$el.find("#content");

            this.breadcrumb_view = null;
            this.header_view = null;
            this.content_view = null;
        },
        render: function() {
            this.$el.html(this.template());
        },

        set_breadcrumb: function(view) {
            if (this.breadcrumb_view !== null) {
                this.breadcrumb_view.remove();
            }
            this.breadcrumb_view = view;
            this.breadcrumb.prepend(this.breadcrumb_view.render().el);
        },
        set_header: function(view) {
            if (this.header_view !== null) {
                this.header_view.remove();
            }
            this.header_view = view;
            this.header.html(this.header_view.render().el);
        },
        set_content: function(view) {
            if (this.content_view !== null) {
                this.content_view.remove();
            }
            this.content_view = view;
            this.content.html(this.content_view.render().el);
        }
    });
    AppView.extend = function(child) {
        var view = Backbone.View.extend.apply(this, arguments);
        view.prototype.events = _.extend({}, this.prototype.events, child.events);
        return view;
    };

    return AppView;
});