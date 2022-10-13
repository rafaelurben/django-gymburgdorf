// API

/// Base methods

const toUrlEncoded = obj => Object.keys(obj).map(k => encodeURIComponent(k) + '=' + encodeURIComponent(obj[k])).join('&');

function api_get(url, callback, type="GET") {
    var request = new XMLHttpRequest();
    request.open(type, url , true);

    request.onload = function () {
        if (request.status == 200) {
            var json = JSON.parse(request.responseText);
            if (!("error" in json)) {
                console.log("[Post] - Success!", json);
                // top.toast({
                //     "titleText": "Anfrage erfolgreich",
                //     "icon": "success",
                // })
                callback(json);
            } else if ("error" in json) {
                console.log("[Post] - Succeeded with error message!", json);
                top.toast({
                    "titleText": "Fehler! " + json.error,
                    "icon": "error",
                })
            } else {
                console.log("[Post] - Succeeded with invalid response!", json);
                top.toast({
                    "titleText": "Fehler!",
                    "icon": "error",
                })
            }
        } else {
            console.error(request.status, request.responseText);
            top.toast({
                "titleText": "Fehler!",
                "icon": "error",
            })
        }
    };

    request.timeout = 5000;

    request.ontimeout = function (event) {
        console.warn("[Receive] - Request timeout!", event);
        top.toast({
            "titleText": "Fehler! (Timeout)",
            "icon": "warning",
        })
    }

    // top.toast({
    //     "titleText": "Anfrage bearbeiten...",
    //     "icon": "info",
    //     "timer": 5000,
    // })
    request.send();
}

function api_delete(url, callback) {
    api_get(url, callback, "DELETE")
}

function api_post(url, data, callback) {
    var request = new XMLHttpRequest();
    request.open('POST', url, true);

    request.onload = function () {
        if (request.status == 200) {
            var json = JSON.parse(request.responseText);
            if (!("error" in json)) {
                console.log("[Post] - Success!", json);
                top.toast({
                    "titleText": "Anfrage erfolgreich",
                    "icon": "success",
                })
                callback(json);
            } else if ("error" in json) {
                console.log("[Post] - Succeeded with error message!", json);
                top.toast({
                    "titleText": "Fehler! "+json.error,
                    "icon": "error",
                })
            } else {
                console.log("[Post] - Succeeded with invalid response!", json);
                top.toast({
                    "titleText": "Fehler!",
                    "icon": "error",
                })
            }
        } else {
            console.error(request.status, request.responseText);
            top.toast({
                "titleText": "Fehler!",
                "icon": "error",
            })
        }
    };
    request.timeout = 5000;

    request.ontimeout = function (event) {
        console.warn("[Post] - Request timeout!");
        top.toast({
            "titleText": "Fehler! (Timeout)",
            "icon": "warning",
        })
    }

    top.toast({
        "titleText": "Anfrage bearbeiten...",
        "icon": "info",
        "timer": 5000,
    })
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    request.send(toUrlEncoded(data));
}

/// Specific methods
//// Manager

function api_grades_get_manager(callback = grades_render) {
    api_get(window.api_grades_base_url, callback);
}

//// Semester

function api_grades_get_semester(id, callback = grades_render) {
    api_get(window.api_grades_base_url+"semester/"+id, callback);
}

function api_grades_create_semester(title, callback = grades_parsePostResponse) {
    api_post(window.api_grades_base_url+"semester/add", {
        title: title,
    }, callback);
}

function api_grades_delete_semester(id, callback = grades_parsePostResponse) {
    api_delete(window.api_grades_base_url+"semester/"+id, callback);
}

//// Subject

function api_grades_get_subject(id, callback = grades_render) {
    api_get(window.api_grades_base_url+"subject/"+id, callback);
}

function api_grades_create_subject(semesterid, title, weight = 1.0, callback = grades_parsePostResponse) {
    api_post(window.api_grades_base_url + "subject/add/" + semesterid, {
        title: title,
        weight: weight,
    }, callback);
}

function api_grades_delete_subject(id, callback = grades_parsePostResponse) {
    api_delete(window.api_grades_base_url+"subject/"+id, callback);
}

//// Grade

function api_grades_get_grade(id, callback = grades_render) {
    api_get(window.api_grades_base_url+"grade/"+id, callback);
}

function api_grades_create_grade(subjectid, title, value, weight = 1.0, is_partial_grade = false, callback = grades_parsePostResponse) {
    api_post(window.api_grades_base_url + "grade/add/" + subjectid, {
        title: title,
        value: value,
        weight: weight,
        is_partial_grade: is_partial_grade || "",
    }, callback);
}

function api_grades_delete_grade(id, callback = grades_parsePostResponse) {
    api_delete(window.api_grades_base_url+"grade/"+id, callback);
}

//// Partial grade

function api_grades_get_partialgrade(id, callback = grades_render) {
    api_get(window.api_grades_base_url+"partialgrade/"+id, callback);
}

function api_grades_create_partialgrade(gradeid, title, value, weight, callback = grades_parsePostResponse) {
    api_post(window.api_grades_base_url+"partialgrade/add/"+gradeid, {
        title: title,
        value: value,
        weight: weight,
    }, callback);
}

function api_grades_delete_partialgrade(id, callback = grades_parsePostResponse) {
    api_delete(window.api_grades_base_url+"partialgrade/"+id, callback);
}

// Navigation and render

grades_navigation = [
    {
        title: "Home",
        type: "grademanager", 
        id: null
    }
]

function grades_navigateUp() {
    grades_navigation.pop();
    grades_reRender();
}

function grades_navigateDown(obj) {
    grades_navigation.push(obj);
    grades_reRender();
}

function grades_reset_display() {
    grades_nav_back = document.getElementById("grades-nav-back");
    grades_nav_info = document.getElementById("grades-nav-info");
    grades_nav_info.innerHTML = "Laden...";
    if (grades_navigation.length === 1) {
        grades_nav_back.style.display = "none";
        grades_nav_back.onclick = () => void 0;
    } else {
        grades_nav_back.style.display = "initial";
        grades_nav_back.onclick = () => grades_navigateUp();
    }
    grades_breadcrumbs = document.getElementById("grades-nav-breadcrumbs");
    grades_breadcrumbs.innerHTML = grades_navigation.map(e => e.title).join(" > ");
    grades_table = document.getElementById("grades-table");
    grades_table.innerHTML = "";
    grades_title = document.getElementById("grades-title");
    grades_title.innerHTML = "Wird geladen...";
}

function grades_render(data) {
    grades_reset_display();

    grades_table = document.getElementById("grades-table");
    grades_title = document.getElementById("grades-title");
    grades_nav_info = document.getElementById("grades-nav-info");
    grades_nav_info.innerHTML = data.info;

    if (data.type === "grademanager") {
        grades_navigation[grades_navigation.length - 1].semesters = data.semesters;
        grades_title.innerHTML = `Start`;
        for (s in data.semesters) {
            obj = data.semesters[s];

            tr = document.createElement("tr");
            tr.setAttribute("data-index", s);
            tr.setAttribute("data-title", `Semester: ${obj.title} (ID: ${obj.id})`);

            td3 = document.createElement("td");
            td3.innerHTML = obj.title;

            tr.appendChild(td3);

            td2 = document.createElement("td");
            td2_i = document.createElement("i");
            td2_i.addEventListener("click", (event) => {
                id = parseInt(event.srcElement.parentElement.parentElement.getAttribute("data-index"));
                obj = grades_navigation[grades_navigation.length - 1].semesters[id];
                top.popup_delete(() => {
                    api_grades_delete_semester(obj.id)
                }, event.srcElement.parentElement.parentElement.getAttribute("data-title"));
            });
            td2_i.className = "fas fa-fw fa-trash";

            td2.appendChild(td2_i);
            tr.insertBefore(td2, td3);

            td1 = document.createElement("td"); 
            td1_i = document.createElement("i");
            td1_i.addEventListener("click", (event) => {
                id = parseInt(event.srcElement.parentElement.parentElement.getAttribute("data-index"));
                obj = grades_navigation[grades_navigation.length - 1].semesters[id];
                grades_navigateDown(obj);
            });
            td1_i.className = "fas fa-fw fa-level-down-alt";

            td1.appendChild(td1_i);
            tr.insertBefore(td1, td2);

            td4 = document.createElement("td");
            td4.innerHTML = obj.value;

            tr.appendChild(td4)

            td5 = document.createElement("td");

            tr.appendChild(td5)

            grades_table.appendChild(tr);
        }

        tr = document.createElement("tr");
        tr.innerHTML = '<td></td><td><i class="fas fa-fw fa-plus-square"></i></td><td>Neues Semester erstellen&nbsp;&nbsp;</td>'
        tr.onclick = () => { create_semester() };

        grades_table.appendChild(tr);

    } else if (data.type === "semester") {
        grades_navigation[grades_navigation.length - 1].subjects = data.subjects;
        grades_title.innerHTML = `Fächerliste`;
        for (s in data.subjects) {
            obj = data.subjects[s];

            tr = document.createElement("tr");
            tr.setAttribute("data-index", s);
            tr.setAttribute("data-title", `Fach: ${obj.title} (ID: ${obj.id})`);

            td3 = document.createElement("td");
            td3.innerHTML = obj.title;

            tr.appendChild(td3);

            td2 = document.createElement("td");
            td2_i = document.createElement("i");
            td2_i.addEventListener("click", (event) => {
                id = parseInt(event.srcElement.parentElement.parentElement.getAttribute("data-index"));
                obj = grades_navigation[grades_navigation.length - 1].subjects[id];
                top.popup_delete(() => {
                    api_grades_delete_subject(obj.id)
                }, event.srcElement.parentElement.parentElement.getAttribute("data-title"));
            });
            td2_i.className = "fas fa-fw fa-trash";

            td2.appendChild(td2_i);
            tr.insertBefore(td2, td3);

            td1 = document.createElement("td");
            td1_i = document.createElement("i");
            td1_i.addEventListener("click", (event) => {
                id = parseInt(event.srcElement.parentElement.parentElement.getAttribute("data-index"));
                obj = grades_navigation[grades_navigation.length - 1].subjects[id];
                grades_navigateDown(obj);
            });
            td1_i.className = "fas fa-fw fa-level-down-alt";

            td1.appendChild(td1_i);
            tr.insertBefore(td1, td2);

            td4 = document.createElement("td");
            td4.innerHTML = obj.value;

            tr.appendChild(td4)

            td5 = document.createElement("td");
            td5.innerHTML = obj.weight;

            tr.appendChild(td5)

            grades_table.appendChild(tr);
        }

        tr = document.createElement("tr");
        tr.innerHTML = '<td></td><td><i class="fas fa-fw fa-plus-square"></i></td><td>Neues Fach erstellen &nbsp;&nbsp;</td>'
        tr.onclick = () => { create_subject(data.id) };

        grades_table.appendChild(tr);

    } else if (data.type === "subject") {
        grades_navigation[grades_navigation.length - 1].grades = data.grades;
        grades_title.innerHTML = `Notenliste`;
        for (g in data.grades) {
            obj = data.grades[g];

            tr = document.createElement("tr");
            tr.setAttribute("data-index", g);
            tr.setAttribute("data-title", `Fach: ${obj.title} (ID: ${obj.id})`);

            td3 = document.createElement("td");
            td3.innerHTML = obj.title;

            tr.appendChild(td3);

            td2 = document.createElement("td");
            td2_i = document.createElement("i");
            td2_i.addEventListener("click", (event) => {
                id = parseInt(event.srcElement.parentElement.parentElement.getAttribute("data-index"));
                obj = grades_navigation[grades_navigation.length - 1].grades[id];
                top.popup_delete(() => {
                    api_grades_delete_grade(obj.id)
                }, event.srcElement.parentElement.parentElement.getAttribute("data-title"));
            });
            td2_i.className = "fas fa-fw fa-trash";

            td2.appendChild(td2_i);
            tr.insertBefore(td2, td3);

            td1 = document.createElement("td");
            if (obj.is_partial_grade) {
                td1_i = document.createElement("i");
                td1_i.addEventListener("click", (event) => {
                    id = parseInt(event.srcElement.parentElement.parentElement.getAttribute("data-index"));
                    obj = grades_navigation[grades_navigation.length - 1].grades[id];
                    grades_navigateDown(obj);
                });
                td1_i.className = "fas fa-fw fa-level-down-alt";
                
                td1.appendChild(td1_i);
            }
            tr.insertBefore(td1, td2);

            td4 = document.createElement("td");
            td4.innerHTML = obj.value;

            tr.appendChild(td4)

            td5 = document.createElement("td");
            td5.innerHTML = obj.weight;

            tr.appendChild(td5)

            grades_table.appendChild(tr);
        }

        tr = document.createElement("tr");
        tr.innerHTML = '<td></td><td><i class="fas fa-fw fa-plus-square"></i></td><td>Neue Note erstellen&nbsp;&nbsp;</td>'
        tr.onclick = () => { create_grade(data.id) };

        grades_table.appendChild(tr);

    } else if (data.type === "grade") {
        grades_navigation[grades_navigation.length - 1].partial_grades = data.partial_grades;
        grades_title.innerHTML = `Teilnotenliste`;
        for (p in data.partial_grades) {
            obj = data.partial_grades[p];

            tr = document.createElement("tr");
            tr.setAttribute("data-index", p);
            tr.setAttribute("data-title", `Teilnote: ${obj.title} (ID: ${obj.id})`);

            td3 = document.createElement("td");
            td3.innerHTML = obj.title;

            tr.appendChild(td3);

            td2 = document.createElement("td");
            td2_i = document.createElement("i");
            td2_i.addEventListener("click", (event) => {
                index = parseInt(event.srcElement.parentElement.parentElement.getAttribute("data-index"));
                obj = grades_navigation[grades_navigation.length - 1].partial_grades[index];
                console.log(obj, index, grades_navigation);
                top.popup_delete(() => {
                    console.log(obj);
                    api_grades_delete_partialgrade(obj.id);
                }, event.srcElement.parentElement.parentElement.getAttribute("data-title"));
            });
            td2_i.className = "fas fa-fw fa-trash";

            td2.appendChild(td2_i);
            tr.insertBefore(td2, td3);

            td1 = document.createElement("td");
            
            tr.insertBefore(td1, td2);

            td4 = document.createElement("td");
            td4.innerHTML = obj.value;

            tr.appendChild(td4)

            td5 = document.createElement("td");
            td5.innerHTML = obj.weight;

            tr.appendChild(td5)

            grades_table.appendChild(tr);
        }

        tr = document.createElement("tr");
        tr.innerHTML = '<td></td><td><i class="fas fa-fw fa-plus-square"></i></td><td>Neue Teilnote erstellen&nbsp;&nbsp;</td>'
        tr.onclick = () => { create_partialgrade(data.id) };

        grades_table.appendChild(tr);

    }

    masonry_resizeAllItems();
    document.getElementById("grades-nav-reload").scrollIntoView()
}

function grades_reRender() {
    grades_reset_display();
    
    renderObj = grades_navigation[grades_navigation.length - 1];
    if (renderObj.type === "grademanager") {
        api_grades_get_manager(grades_render);
    } else if (renderObj.type === "semester") {
        api_grades_get_semester(renderObj.id, grades_render);
    } else if (renderObj.type === "subject") {
        api_grades_get_subject(renderObj.id, grades_render);
    } else if (renderObj.type === "grade") {
        api_grades_get_grade(renderObj.id, grades_render);
    }
    
    masonry_resizeAllItems();
}

function grades_parsePostResponse(data) {
    if (data.success) {
        grades_reRender();
    }
}

window.addEventListener("load", () => grades_reRender());

// Swal

async function create_semester(callback = grades_parsePostResponse) {
    const { value: formValues } = await top.Swal.fire({
        title: 'Semester erstellen',
        html:
            '<input id="input-title" class="swal2-input" type="text" placeholder="Titel">',
        focusConfirm: false,
        allowOutsideClick: false,
        allowEscapeKey: false,
        showCancelButton: true,
        confirmButtonText: "Speichern",
        cancelButtonText: "Abbrechen",
        preConfirm: () => {
            data = {
                title: top.Swal.getContent().querySelector('#input-title').value,
            },
            api_grades_create_semester(title = data.title, callback = callback);
            return data;
        },
    })

    return formValues;
}

async function create_subject(semesterid, callback = grades_parsePostResponse) {
    const { value: formValues } = await top.Swal.fire({
        title: 'Fach erstellen',
        html:
            '<input id="input-title"  class="swal2-input" type="text" placeholder="Titel">' +
            '<label for="input-weight">Gewicht</label><br>' +
            '<input id="input-weight" class="swal2-input" type="number" value="1.0" step="0.1" min="0.0" max="2.0">',
        focusConfirm: false,
        allowOutsideClick: false,
        allowEscapeKey: false,
        showCancelButton: true,
        confirmButtonText: "Speichern",
        cancelButtonText: "Abbrechen",
        preConfirm: () => {
            data = {
                title: top.Swal.getContent().querySelector('#input-title').value,
                weight: parseFloat(top.Swal.getContent().querySelector('#input-weight').value),
            },
            api_grades_create_subject(semesterid, title = data.title, weight = data.weight, callback=callback);
            return data;
        },
    })

    return formValues;
}

async function create_grade(subjectid, callback = grades_parsePostResponse) {
    const { value: formValues } = await top.Swal.fire({
        title: 'Note erstellen',
        html:
            '<input id="input-title"  class="swal2-input" type="text" placeholder="Titel">' +
            '<label for="input-weight">Gewicht</label><br>' +
            '<input id="input-weight" class="swal2-input" type="number" value="1.0" step="0.1" min="0.0" max="2.0">' +
            '<br><label for="input-is_partial_grade">Teilnote?</label><br>' +
            '<input id="input-is_partial_grade" class="swal2-input" type="checkbox">' +
            '<br><label for="input-value" id="label-input-value">Note</label><br>' +
            '<input id="input-value" class="swal2-input" type="number" value="4.0" step="0.1" min="0.0" max="6.0">',
        focusConfirm: false,
        input: 'range',
        inputValue: 4.0,
        inputAttributes: {
            min: 0,
            max: 6,
            step: 0.1,
        },
        allowOutsideClick: false,
        allowEscapeKey: false,
        showCancelButton: true,
        confirmButtonText: "Speichern",
        cancelButtonText: "Abbrechen",
        preConfirm: () => {
            data = {
                title: top.Swal.getContent().querySelector('#input-title').value,
                weight: parseFloat(top.Swal.getContent().querySelector('#input-weight').value),
                is_partial_grade: top.Swal.getContent().querySelector('#input-is_partial_grade').checked,
                value: parseFloat(top.Swal.getContent().querySelector('#input-value').value),
            },
            api_grades_create_grade(subjectid, title = data.title, value = data.value, weight = data.weight, is_partial_grade = data.is_partial_grade, callback=callback);
            return data;
        },
        didOpen: () => {
            const inputRange = top.Swal.getInput()
            const inputNumber = top.Swal.getContent().querySelector('#input-value')
            const inputCheckmark = top.Swal.getContent().querySelector('#input-is_partial_grade')
            const label = top.Swal.getContent().querySelector('#label-input-value')

            // remove default output
            inputRange.nextElementSibling.style.display = 'none'
            inputRange.style.width = '100%'

            // sync input[type=number] with input[type=range]
            inputRange.addEventListener('input', () => {
                inputNumber.value = inputRange.value
            })

            // sync input[type=range] with input[type=number]
            inputNumber.addEventListener('change', () => {
                inputRange.value = inputNumber.value
            })

            inputCheckmark.addEventListener('input', () => {
                if (inputCheckmark.checked) {
                    inputRange.style.display = 'none';
                    inputNumber.style.display = 'none';
                    label.style.display = 'none';
                } else {
                    inputRange.style.display = 'initial';
                    inputNumber.style.display = 'initial';
                    label.style.display = 'initial';
                }
            })
        }
    })

    return formValues;
}


async function create_partialgrade(gradeid, callback = grades_parsePostResponse) {
    const { value: formValues } = await top.Swal.fire({
        title: 'Teilnote erstellen',
        html:
            '<input id="input-title"  class="swal2-input" type="text" placeholder="Titel">' +
            '<label for="input-weight">Gewicht</label><br>' +
            '<input id="input-weight" class="swal2-input" type="number" value="1.0" step="0.1" min="0.0" max="2.0">' +
            '<br><label for="input-value">Note</label><br>' +
            '<input id="input-value"  class="swal2-input" type="number" value="4.0" step="0.1" min="0.0" max="6.0">',
        focusConfirm: false,
        input: 'range',
        inputValue: 4.0,
        inputAttributes: {
            min: 0,
            max: 6,
            step: 0.1,
        },
        allowOutsideClick: false,
        allowEscapeKey: false,
        showCancelButton: true,
        confirmButtonText: "Speichern",
        cancelButtonText: "Abbrechen",
        preConfirm: () => {
            data = {
                title: top.Swal.getContent().querySelector('#input-title').value,
                weight: parseFloat(top.Swal.getContent().querySelector('#input-weight').value),
                value: parseFloat(top.Swal.getContent().querySelector('#input-value').value),
            },
            api_grades_create_partialgrade(gradeid, title=data.title, value=data.value, weight=data.weight, callback=callback);
            return data;
        },
        didOpen: () => {
            const inputRange = top.Swal.getInput()
            const inputNumber = top.Swal.getContent().querySelector('#input-value')

            // remove default output
            inputRange.nextElementSibling.style.display = 'none'
            inputRange.style.width = '100%'

            // sync input[type=number] with input[type=range]
            inputRange.addEventListener('input', () => {
                inputNumber.value = inputRange.value
            })

            // sync input[type=range] with input[type=number]
            inputNumber.addEventListener('change', () => {
                inputRange.value = inputNumber.value
            })
        }
    })

    return formValues;
}
