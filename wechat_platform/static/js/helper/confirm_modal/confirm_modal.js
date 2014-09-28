define(['jquery', 'backbone', 'bootstrap'], function($, Backbone) {
    var ConfirmModalView = Backbone.View.extend({
        el: "#confirm-modal",
        events: {
            "click .btn-ok": "run_callback",
            "click .btn-cancel": "hide"
        },
        show: function(args) {
            this.$el.find(".modal-title").html(args.title);
            this.$el.find(".modal-body").html("<p>" + args.body + "</p>");
            this.cb = args.cb;

            this.$el.modal("show");
        },
        hide: function() {
            this.$el.modal("hide");
        },
        run_callback: function() {
            this.cb();
            this.$el.modal("hide");
        }
    });

    return ConfirmModalView;
});