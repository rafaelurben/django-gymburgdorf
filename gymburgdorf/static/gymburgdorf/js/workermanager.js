// <editor-fold> Notifications

function notifications_askForPerm() {
    console.log("[Notifications] - Asking for permissions...");
    return Notification.requestPermission().then(result => {
        if (result.permission === "granted" || result === "granted") {
            /* do our magic */
            console.log("[Notifications] - Permission granted!");
            return true;
        }
        return false;
    });
}

function notifications_getPerm() {
    if (Notification.permission === "granted") {
        console.log("[Notifications] - Permission granted!");
        /* do our magic */
        return true;
    } else if (Notification.permission === "denied" || Notification.permission === "blocked") {
        console.warn("[Notifications] - Permission denied!");
        /* the user has previously denied push. Can't reprompt. */
        return false;
    } else {
        console.log("[Notifications] - Permission unset!");
        /* show a prompt to the user */
        return null;
    }
}

function notifications_displayNotification() {
    if (Notification.permission == 'granted') {
        navigator.serviceWorker.getRegistration().then(function(reg) {
            var options = {
                body: 'Dies ist eine Testnachricht!',
                icon: '../../static/gymburgdorf/favicon.ico',
                vibrate: [100, 50, 100],
                data: {
                    dateOfArrival: Date.now(),
                    primaryKey: '2'
                },
                actions: [{
                        action: 'open',
                        title: 'Webseite öffnen'
                    },
                    {
                        action: 'close',
                        title: 'Schliessen'
                    },
                ],
                tag: "1",
            };

            reg.showNotification('Hallo Welt!', options);

        });
    }
}

// </editor-fold> Notifications

// <editor-fold> Subscription

function urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

function subscription_upload(sub, url, showToast = true, after = null) {
    var data = JSON.stringify(sub.toJSON());

    console.log("[Subscription] - Uploading subscription to", url);

    var xhr = new XMLHttpRequest();

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log("[Subscription] - Uploaded!")
            if (showToast) {
                toast({
                    titleText: "Mitteilungen aktiviert!",
                    icon: "success"
                })
            }
            if (after !== null) {
                after();
            }
        } else if (xhr.readyState === 4) {
            console.error("[Subscription] - Upload failed!")
            if (showToast) {
                toast({
                    titleText: "Aktivieren fehlgeschlagen!",
                    icon: "error"
                })
            }
        }
    };
    xhr.send(data);
}

function subscription_delete(sub, url, after = null) {
    var data = JSON.stringify(sub.toJSON());

    console.log("[Subscription] - Deleting subscription at", url);

    var xhr = new XMLHttpRequest();

    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log("[Subscription] - Deleted!")
            toast({
                titleText: "Mitteilungen deaktiviert!",
                icon: "info"
            })
            if (after !== null) {
                after();
            }
        } else if (xhr.readyState === 4) {
            console.error("[Subscription] - Deletion failed!")
            toast({
                titleText: "Deaktivieren fehlgeschlagen!",
                icon: "error"
            })
        }
    };
    xhr.send(data);
}

function subscription_subscribe(after = null) {
    if ('serviceWorker' in navigator && "Notification" in window) {
        navigator.serviceWorker.ready.then(function(reg) {
            var options = {
                userVisibleOnly: true
            };
            if (window.hasOwnProperty("applicationServerKey") && window.applicationServerKey) {
                options.applicationServerKey = urlB64ToUint8Array(window.applicationServerKey);
            }
            reg.pushManager.subscribe(options).then(function(sub) {
                console.log("[Subscription] - Subscribed:", sub.toJSON())
                toast({
                    titleText: "Mitteilungen aktivieren...",
                })
                subscription_upload(sub, window.subscriptionUploadUrl, showToast = true, after = after);
            }).catch(function(e) {
                if (Notification.permission === 'denied' || Notification.permission === 'blocked') {
                    console.warn('[Subscription] - Error: No permission!');
                } else {
                    console.error('[Subscription] - Error:', e);
                }
            });
        })
    }
}

function subscription_unsubscribe(after = null) {
    if ('serviceWorker' in navigator && "Notification" in window) {
        navigator.serviceWorker.ready.then(function(reg) {
            reg.pushManager.getSubscription().then(function(sub) {
                if (sub !== null) {
                    sub.unsubscribe();
                    console.log("[Subscription] - Unsubscribed!");
                    toast({
                        titleText: "Mitteilungen deaktivieren...",
                    });
                    subscription_delete(sub, window.subscriptionDeleteUrl, after = after);
                } else {
                    console.warn("[Subscription] - Wasn't subscribed before!");
                    toast({
                        titleText: "Mitteilungen waren gar nicht aktiv!",
                        icon: "error"
                    });
                }
            });
        })
    }
}

// </editor-fold> Subscription

// <editor-fold> App Install

let deferredPrompt = null;

var askForAppInstall = function() {
    if (deferredPrompt !== null) {
        console.log("[APP] - Asking user for app install...")
        Swal.fire({
            title: 'Diese Seite als App installieren',
            html: "<p>Scheinbar unterstützt dein Gerät das installieren von sogenannten 'Progressive Web Apps'. Somit kannst du diese Webseite zu deinem Homebildschirm hinzufügen und wie eine normale App verwenden.</p><br>" +
                "<h4>Vorteile:</h4>" +
                "<p>Offline-Funktion<p><p>Push-Mitteilungen (w.i.p)</p><br>" +
                "<h4>Hinweis:</h4>" +
                "<p>Nicht alle Funktionen sind auf allen Geräten verfügbar!</p>",
            // icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'App installieren!',
            cancelButtonText: 'Schliessen'
        }).then((result) => {
            if (result.value) {
                console.log("[APP] - Showing install prompt...")
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('[APP] - User accepted the install prompt!');
                    } else {
                        console.log('[APP] - User dismissed the install prompt!');
                    }
                });

                try {
                    const iframe = document.getElementById("iframe-home").contentWindow;
                    iframe.document.body.classList.remove("app-installable");
                    iframe.masonry_resizeAllItems();
                } catch (error) {
                    console.log("[App] - The install-message couldn't be hidden!", error)
                }
            } else {
                console.log("[APP] - User doesn't want to install the app.")
            }
        })
    } else {
        try {
            const iframe = document.getElementById("iframe-home").contentWindow;
            iframe.document.body.classList.remove("app-installable");
            iframe.masonry_resizeAllItems();
        } catch (error) {
            console.log("[App] - The install-message couldn't be hidden!", error)
        }
    }
}

window.addEventListener('beforeinstallprompt', event => {
    event.preventDefault();
    deferredPrompt = event;
    console.log("[APP] - Promt may now be shown! Possible Platforms:", event.platforms);

    try {
        const iframe = document.getElementById("iframe-home").contentWindow;
        iframe.document.body.classList.add("app-installable");
        iframe.masonry_resizeAllItems();
    } catch (error) {
        console.log("[App] - The install-message couldn't be shown!", error)
    }
});

window.addEventListener('appinstalled', event => {
    console.log('[APP] - Successfully installed!');
});

// </editor-fold> App install

// <editor-fold> Service Worker Init

window.addEventListener("load", function() {
    if ('serviceWorker' in navigator && window.hasOwnProperty("serviceWorkerUrl")) {
        navigator.serviceWorker.register(window.serviceWorkerUrl, {
            scope: '/'
        }).then(function(registration) {
            console.log('[APP] - Service worker registered with scope', registration.scope);
            registration.update();
            registration.pushManager.getSubscription().then(function(sub) {
                if (sub === null) {
                    console.warn('[Subscription] - Not subscribed to push service!');
                    // Update UI to ask user to register for Push
                } else if (window.hasOwnProperty("subscriptionUploadUrl")) {
                    subscription_upload(sub, window.subscriptionUploadUrl, showToast = false);
                }
            });
        }).catch(function(error) {
            console.log('[APP] - Service worker registration failed, error:', error);
        });
    }

    if ('Notification' in window && 'serviceWorker' in navigator) {
        console.log("[Notifications] - Supported!");
    }
})

// </editor-fold> Service Worker Init