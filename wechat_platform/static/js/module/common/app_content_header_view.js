define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');

    var ContentHeaderView = Backbone.View.extend({
        initialize: function (args) {
            this.template = _.template(args.html);
            if (args.hasOwnProperty('data')) {
                this.data = args.data;
            }
        },
        render: function () {
            if (this.hasOwnProperty('data')) {
                this.$el.html(this.template(this.data));
            } else {
                this.$el.html(this.template());
            }
            return this;
        }
    });

    return ContentHeaderView;
});