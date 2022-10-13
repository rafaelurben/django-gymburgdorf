function navbar_hide(timeout = 0, enable_scroll = true) {
    document.getElementById('navbar-toggle').classList.remove('open');
    setTimeout(function() {
        if (enable_scroll) {
            scroll_enable();
        }
        document.getElementById('navbar').classList.remove('open');
        document.getElementById('navbar-menu').classList.remove('open');
        // document.getElementById("header-image").classList.remove('hide');
    }, timeout);
};

function navbar_show(timeout = 0, disable_scroll = true) {
    if (disable_scroll) {
        scroll_disable();
    }
    document.getElementById('navbar-toggle').classList.add('open');
    setTimeout(function() {
        document.getElementById('navbar').classList.add('open');
        document.getElementById('navbar-menu').classList.add('open');
        // document.getElementById("header-image").classList.add('hide');
    }, timeout);
};

function navbar_toggle(modify_scroll = true) {
    if (document.getElementById('navbar').classList.contains('open')) {
        navbar_hide(200, modify_scroll);
    } else {
        navbar_show(200, modify_scroll);
    }
};



function navbar_scroll() {
    document.getElementById("navbar").scrollIntoView({
        behavior: 'smooth'
    });
};



function scroll_disable() {
    document.body.classList.add("noscroll");
};

function scroll_enable() {
    document.body.classList.remove("noscroll");
};

function scroll_toggle() {
    document.body.classList.toggle('noscroll');
};

// Pull to refresh (mobile)

var pStart = {
    x: 0,
    y: 0
};
var pStop = {
    x: 0,
    y: 0
};

function swipeStart(e) {
    if (typeof e['targetTouches'] !== "undefined") {
        var touch = e.targetTouches[0];
        pStart.x = touch.screenX;
        pStart.y = touch.screenY;
    } else {
        pStart.x = e.screenX;
        pStart.y = e.screenY;
    }
}

function swipeEnd(e) {
    if (typeof e['changedTouches'] !== "undefined") {
        var touch = e.changedTouches[0];
        pStop.x = touch.screenX;
        pStop.y = touch.screenY;
    } else {
        pStop.x = e.screenX;
        pStop.y = e.screenY;
    }

    swipeCheck();
}

function swipeIsPullDown(dY, dX) {
    return dY < 0 && (
        (Math.abs(dX) <= 100 && Math.abs(dY) >= 300) ||
        (Math.abs(dX) / Math.abs(dY) <= 0.3 && dY >= 60)
    );
}


function swipeCheck() {
    var changeY = pStart.y - pStop.y;
    var changeX = pStart.x - pStop.x;

    if (swipeIsPullDown(changeY, changeX) && navigator.onLine) {
        document.getElementById("loading-container").classList.add("visible");
        setTimeout(function() {
            window.location.reload(true);
        }.bind(window.location), 200);
    }
}

document.addEventListener('touchstart', function(e) {
    swipeStart(e);
}, false);
document.addEventListener('touchend', function(e) {
    swipeEnd(e);
}, false);