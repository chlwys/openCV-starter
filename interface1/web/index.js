eel.setup()

eel.expose(updateImageSrc)
function updateImageSrc(val, id) {
  let elem = document.getElementById(id);
  elem.src = "data:image/jpeg;base64," + val;
}
