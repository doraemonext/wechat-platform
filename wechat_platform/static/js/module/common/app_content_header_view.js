define(function(require, exports, module) {
    var $ = require('jquery');
    var Backbone = require('backbone');

    var ContentHeaderView = Backbone.View.extend({
        initialize: function (args) {
            this.template = _.template(args.html);
        },
        render: function () {
            this.$el.html(this.template());
            return this;
        }
    });

    return ContentHeaderView;
});