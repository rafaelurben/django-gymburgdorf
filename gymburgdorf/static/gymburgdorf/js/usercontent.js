function showUserContentSwal(object) {
    data = {
        title: object.kategorie_display + ' #' + object.id,
        text: object._fullinfo,
        footer: "Eingereicht von: " + object.username,
        customClass: {
            content: 'preservelines'
        },
        showCancelButton: true,
        cancelButtonText: "Schliessen",
        showDenyButton: object.candelete,
        denyButtonText: "Löschen",
        showConfirmButton: object.canpublish,
        confirmButtonText: "Veröffentlichen",
    }

    Swal.fire(data).then(function (result) {
        if (result.isConfirmed) {
            Swal.fire({
                icon: "question",
                title: "Veröffentlichen?",
                text: "Soll dieses Objekt veröffentlicht werden?",
                showConfirmButton: true,
                confirmButtonText: "Veröffentlichen",
                showCancelButton: true,
                cancelButtonText: "Abbrechen",
            }).then(function (result2) {
                if (result2.isConfirmed) {
                    $.post(
                        url = window.api_usercontent_base_url+"publish",
                        data = {id: object.id}
                    ).done(function () {
                        toast({
                            title: 'Erfolgreich veröffentlicht',
                            icon: 'success'
                        })
                        loadUserContent(noloading = true);
                    }).fail(function () {
                        toast({
                            title: 'Veröffentlichen fehlgeschlagen!',
                            icon: 'error'
                        })
                    })
                }
            })
        } else if (result.isDenied) {
            Swal.fire({
                icon: "warning",
                title: "Löschen?",
                text: "Dieses Objekt wirklich löschen? (dies kann nicht rückgängig gemacht werden)",
                showConfirmButton: true,
                confirmButtonText: "Löschen",
                showCancelButton: true,
                cancelButtonText: "Schliessen",
            }).then(function (result2) {
                if (result2.isConfirmed) {
                    $.post(
                        url = window.api_usercontent_base_url + "delete",
                        data = { id: object.id }
                    ).done(function () {
                        toast({
                            title: 'Erfolgreich gelöscht',
                            icon: 'success'
                        })
                        loadUserContent(noloading = true);
                    }).fail(function () {
                        toast({
                            title: 'Löschen fehlgeschlagen!',
                            icon: 'error'
                        })
                    })
                }
            })
        }
    })
}

function suggestUserContent() {
    Swal.mixin({
        confirmButtonText: 'Weiter &rarr;',
        showCancelButton: true,
        cancelButtonText: "Abbrechen",
        allowOutsideClick: false,
        allowEscapeKey: false,
        progressSteps: ['1', '2', '3', '4'],
    }).queue([
        {
            input: 'select',
            title: 'Kategorie',
            text: 'Bitte wähle eine Kategorie:',
            inputValue: 'quote',
            inputOptions: window.usercontentcategories,
        },
        {
            input: 'text',
            title: 'Titel',
            text: 'Kurze Zusammenfassung',
            inputValidator: (value) => {
                return new Promise((resolve) => {
                    if (value.length > 5) {
                        resolve()
                    } else {
                        resolve('Das ist ein bisschen zu kurz...')
                    }
                })
            },
            inputAttributes: {
                max: 50,
            }
        },
        {
            input: 'textarea',
            title: 'Beschreibung',
            text: 'Kompletter Inhalt',
            inputValidator: (value) => {
                return new Promise((resolve) => {
                    if (value.length > 5) {
                        resolve()
                    } else {
                        resolve('Das ist ein bisschen zu kurz...')
                    }
                })
            }
        },
        {
            input: 'text',
            title: "Person(en)",
            text: "Z.B. Lehrer",
            inputValidator: (value) => {
                return new Promise((resolve) => {
                    if (value.length > 1) {
                        resolve()
                    } else {
                        resolve('Wer ist das?')
                    }
                })
            },
            inputAttributes: {
                max: 250,
            }
        },
    ]).then((result) => {
        if (result.value) {
            console.log(result.value);

            $.post(
                url = window.api_usercontent_base_url + "suggest",
                data = {
                    'kategorie': result.value[0],
                    'titel': result.value[1],
                    'beschreibung': result.value[2],
                    'personen': result.value[3],
                },
            ).done(function () {
                toast({
                    title: 'Erfolgreich hinzugefügt',
                    icon: 'success'
                })
                loadUserContent(noloading = true);
            }).fail(function () {
                toast({
                    title: 'Hinzufügen fehlgeschlagen!',
                    icon: 'error'
                })
            })
        }
    })
}

function loadUserContent(noloading = false) {
    if (!noloading) {
        toast({
            title: 'Laden...',
            icon: 'info',
        })
    }
    $.get(
        url = window.api_usercontent_base_url,
        success = function (data) {
            console.log(data);

            $quotes = $('#quotes').empty();
            $giftideas = $('#giftideas').empty();
            data.objects.forEach(function (object) {
                $tr = $('<tr></tr>').attr('tabindex', 3).attr('class', object.kategorie);
                $tr.append($('<td></td>').text(object.titel))
                $tr.append($('<td></td>').text(object.personen))
                $tr.append($('<td></td>').text(object.beschreibung))
                $tr.append($('<td></td>').text(object.username))

                if (object.kategorie === "quote") {
                    $quotes.append($tr);
                } else if (object.kategorie === "giftidea") {
                    $giftideas.append($tr);
                }
                
                $tr.click(function () {
                    showUserContentSwal(object);
                })
            })

            $verifyqueue = $('#verifyqueue').empty();
            data.verifyqueue.forEach(function (object) {
                $tr = $('<tr></tr>').attr('tabindex', 3);
                $tr.append($('<td></td>').text(object.titel))
                $tr.append($('<td></td>').text(object.personen))
                $tr.append($('<td></td>').text(object.beschreibung))
                $tr.append($('<td></td>').text(object.username))

                $verifyqueue.append($tr);

                $tr.click(function () {
                    showUserContentSwal(object);
                })
            })

            $myobjects = $('#myobjects').empty();
            data.myobjects.forEach(function (object) {
                $tr = $('<tr></tr>').attr('tabindex', 3);
                $tr.append($('<td></td>').text(object.titel))
                $tr.append($('<td></td>').text(object.personen))
                $tr.append($('<td></td>').text(object.kategorie_display))
                $tr.append($('<td></td>').append(object.published ?
                    $("<i></i>").attr('class', 'fas fa-lock-open') : 
                    $("<i></i>").attr('class', 'fas fa-clock')))

                $myobjects.append($tr);

                $tr.click(function () {
                    showUserContentSwal(object);
                })
            })
        }
    ).done(function () {
        masonry_resizeAllItems();
        toast({
            title: 'Erfolgreich geladen',
            icon: 'success',
        })
    }).fail(function () {
        toast({
            title: 'Laden fehlgeschlagen!',
            icon: 'error',
        })
    })
}