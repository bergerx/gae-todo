var add_box_shown=0;

function show_add_form() {
    if (add_box_shown != 1) {
        $('#hider-div').show();
        $('#add-form .default-hidden').slideDown('slow');
        add_box_shown = 1;
    }
    $('html, body').animate({
        scrollTop: $('#add-form').offset().top - $('.navbar-fixed-top').height()
    }, 500, function () {
        $('#add-box').focus();
    });
}

function hide_add_form() {
    if (add_box_shown == 1) {
        $('#hider-div, legend.default-hidden').slideUp('slow', function () {
            $('#add-form .default-hidden').hide();
        })
        $('#add-box').blur();
        add_box_shown = 0;
    }
}

$('.show-add-form').click(show_add_form).keyup(function(e) {
    if (e.keyCode == 27) { // esc
        hide_add_form();
    }
});

$('.hide-add-form').click(hide_add_form);

$('.show-list').click(function () {
    $('html, body').animate({
        scrollTop: $('.items').offset().top - $('.navbar-fixed-top').height()
    }, 500)
});

$('.item').on('click', function () {
    $('div.detail', this).slideToggle();
})