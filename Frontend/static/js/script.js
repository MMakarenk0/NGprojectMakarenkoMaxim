function getToken(){
  const tokenInput = document.getElementById("token-input");
  const token = tokenInput.value;
  return token;
}


document.getElementById("image-upload").addEventListener("change", function(event) {
  var input = event.target;
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      document.getElementById("preview-image").src = e.target.result;

      const fileInput = document.getElementById("image-upload");
      const file = fileInput.files[0];

      const token = getToken();

      const formData = new FormData();
      formData.append("file", file);
      formData.append("token", token);

      const xhttp = new XMLHttpRequest();

      xhttp.onload = function() {
        if (xhttp.status === 200) {
          console.log("File successfully uploaded to the server.");
          var response = xhttp.responseText;
        } else {
          console.log("Error uploading file to the server:", xhttp.status);
        }
      };

      xhttp.open("POST", "http://192.168.1.104:8083/upload", true);
      xhttp.send(formData);
    };
    reader.readAsDataURL(input.files[0]);
  }
});


function invertImage() {
  const token = getToken();

  const formData = new FormData();
  formData.append("token", token);

  const xhttp = new XMLHttpRequest();

  xhttp.onload = function() {
    if (xhttp.status === 200) {
      console.log("File successfully uploaded to the server.");
      var response = xhttp.responseText;

      document.getElementById("preview-image").src = response + "?" + new Date().getTime();
    } else {
      console.log("Error uploading file to the server:", xhttp.status);
    }
  };

  xhttp.open("POST", "http://192.168.1.104:8083/invertImage", true);
  xhttp.send(formData);
}


function extendLifeTime() {
  const token = getToken();
  const formData = new FormData();
  formData.append("token", token);
  
  
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function() {
    if (xhttp.status === 200) {
      console.log("Life time extended");
      var response = xhttp.responseText;
    }
  }
  xhttp.open("POST", "http://192.168.1.104:8083/extendLifeTime", true);
  xhttp.send(formData);
}

window.setInterval(() => {
  extendLifeTime();
}, 60000);

