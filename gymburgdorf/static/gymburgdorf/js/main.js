const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})

const content = $('#content');
const contentscripts = $('#contentscripts');

function toast(options) {
    Toast.fire(options);
}

function randombg() {
    var banners = [
        "url('https://static.wixstatic.com/media/8e1d34_803ac992e50d4f1dacb988d95576641a~mv2.jpg')",
        "url('https://static.wixstatic.com/media/1ac979_f3faf687725d4351ace1e4a9c9a929f6~mv2.jpg')"
    ];
    var random = Math.floor(Math.random() * banners.length) + 0;
    document.getElementById("header-image").style.backgroundImage = banners[random];
};

function loadPage(event = null) {
    var pagename = window.location.hash.replace("#", "");
    var link = document.getElementById("link-" + pagename);

    if (link) {
        navbar_hide();
        navbar_scroll();
        $.get(pagename, function (html) {
            var doc = $(html);
            contentscripts.empty().append(doc.find('script'));
            content.empty().append(doc);
        }).done(function() {
            masonry_resizeAllItems();
            navbar_scroll();
        }).fail(function() {
            toast({icon: 'error', title: 'Error', text: 'Seite konnte nicht geladen werden!'});
            window.location.hash = "home";
        });
    } else {
        toast({ icon: 'error', title: 'Error', text: 'Unbekannte Seite: '+pagename });
        window.location.hash = "home";
    }
};

function handleNetworkChange(event = null) {
    if (navigator.onLine) {
        document.body.classList.remove("offline");
        toast({
            titleText: "Du bist online!",
            text: "Lade neu...",
            icon: "success",
        });
        setTimeout(window.location.reload.bind(window.location), 1000);
    } else {
        document.body.classList.add("offline");
        toast({
            titleText: "Du bist offline!",
            icon: "warning",
        })
    }
}

// Events

window.addEventListener("online", handleNetworkChange);
window.addEventListener("offline", handleNetworkChange);

window.addEventListener("load", () => {
    if (!navigator.onLine) handleNetworkChange();

    randombg();
    if (!Boolean(window.location.hash.replace("#", ""))) {
        window.location.hash = "home";
    } else {
        loadPage();
    }
});

window.addEventListener("hashchange", loadPage);

// Popups

// function popup_news(title, text, url, erstellt_am, disableBackgroundScroll = true) {
//     var data = {
//         titleText: title,
//         footer: "<p>Erstellt: <a>" + erstellt_am + "</a></p>",
//         html: "<p onclick='top.Swal.close()'>" + text + "</p>",
//         showConfirmButton: false,
//         customClass: {
//             footer: 'swalfootermultiline'
//         },
//     }
//     if (url) {
//         data.footer += '<p>Mehr Infos:&nbsp;<a target="_blank" href="' + url + '">' + url + '</a></p>';
//     }
//     if (disableBackgroundScroll) {
//         scroll_disable();
//         data.onAfterClose = scroll_enable;
//     }
//     Swal.fire(data);
// };

// function popup_user(name, biografie, url, imageUrl, disableBackgroundScroll = true) {
//     var data = {
//         titleText: name,
//         html: "<p onclick='top.Swal.close()'>" + biografie + "</p>",
//         showConfirmButton: false,
//         customClass: {
//             footer: 'swalfootermultiline'
//         },
//     }
//     if (url) {
//         data.footer = 'Mehr erfahren:&nbsp;<a target="_blank" href="' + url + '">' + url + '</a>';
//     }
//     if (imageUrl && navigator.onLine) {
//         data.imageUrl = imageUrl;
//         data.imageWidth = "90%";
//         data.imageAlt = "Profilbild von " + name;
//     }
//     if (disableBackgroundScroll) {
//         scroll_disable();
//         data.onAfterClose = scroll_enable;
//     }
//     Swal.fire(data);
// };

// function popup_event(title, text, ort, datum, url, imageUrl, disableBackgroundScroll = true) {
//     var data = {
//         titleText: title,
//         html: "<p onclick='top.Swal.close()'>" + text + "</p>",
//         footer: "<p>Datum: <a>" + datum + "</a></p><p>Ort: <a>" + ort + "</a></p>",
//         showConfirmButton: false,
//         customClass: {
//             footer: 'swalfootermultiline'
//         },
//     }
//     if (url) {
//         data.footer += '<p>Mehr Infos:&nbsp;<a target="_blank" href="' + url + '">' + url + '</a></p>';
//     }
//     if (imageUrl && navigator.onLine) {
//         data.imageUrl = imageUrl;
//         data.imageWidth = "90%";
//     }
//     if (disableBackgroundScroll) {
//         scroll_disable();
//         data.onAfterClose = scroll_enable;
//     }
//     Swal.fire(data);
// };

function popup_delete(callback, text, disableBackgroundScroll = true) {
    var data = {
        title: 'Wirklich löschen?',
        html: 
            "Möchtest du folgendes Objekt wirklich löschen?<br><br>" + 
            text +
            "<br><br>Damit werden auch untergeordnete Elemente gelöscht!",
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Ja, löschen!',
        cancelButtonText: "Abbrechen"
    }

    if (disableBackgroundScroll) {
        scroll_disable();
    }

    Swal.fire(data).then(result => {
        if (disableBackgroundScroll) {
            scroll_enable();
        }
        if (result.value) {
            callback();
        } else {
            toast({
                titleText: "Abgebrochen",
                icon: "info"
            })
        }
    });
}