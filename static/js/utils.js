function getById(id) {
    return document.getElementById(id);
}

function getById4Value(id) {
    return document.getElementById(id).value;
}

function getByName(name) {
    return document.getElementsByName(name);
}

function getByName4Value(name) {
    return document.getElementsByName(name).values();
}

function divHide(id) {
    document.getElementById(id).style.display = 'none';
}

function divNoHide(id) {
    document.getElementById(id).style.display = 'block';
}

function pwd_64(value,id) {
    document.getElementById(id).value = 'p' + btoa(value.value) + '-='
}