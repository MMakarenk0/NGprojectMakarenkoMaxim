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

let timeoutId;

const input_R = document.getElementById('R-input');
input_R.addEventListener('input', function() {
  clearTimeout(timeoutId);

  timeoutId = setTimeout(function() {
    const value_R = input_R.value;
    const token = getToken();
    const formData = new FormData();
    formData.append("token", token);
    formData.append("value_R", value_R);

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
      if (xhttp.status === 200) {
        console.log('Request successful');
        var response = xhttp.responseText;

        document.getElementById("preview-image").src = response + "?" + new Date().getTime();
      } else {
        console.error('Request failed. Error code: ' + xhttp.status);
      }
    }
    xhttp.open("POST", "http://192.168.1.104:8083/colorshift", true);
    xhttp.send(formData);
  }, 500);
});

const input_G = document.getElementById('G-input');
input_G.addEventListener('input', function() {
  clearTimeout(timeoutId);

  timeoutId = setTimeout(function() {
    const value_G = input_G.value;
    const token = getToken();
    const formData = new FormData();
    formData.append("token", token);
    formData.append("value_G", value_G);

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
      if (xhttp.status === 200) {
        console.log('Request successful');
        var response = xhttp.responseText;

        document.getElementById("preview-image").src = response + "?" + new Date().getTime();
      } else {
        console.error('Request failed. Error code: ' + xhttp.status);
      }
    }
    xhttp.open("POST", "http://192.168.1.104:8083/colorshift", true);
    xhttp.send(formData);
  }, 500);
});


const input_B = document.getElementById('B-input');
input_B.addEventListener('input', function() {
  clearTimeout(timeoutId);

  timeoutId = setTimeout(function() {
    const value_B = input_B.value;
    const token = getToken();
    const formData = new FormData();
    formData.append("token", token);
    formData.append("value_B", value_B);

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
      if (xhttp.status === 200) {
        console.log('Request successful');
        var response = xhttp.responseText;

        document.getElementById("preview-image").src = response + "?" + new Date().getTime();
      } else {
        console.error('Request failed. Error code: ' + xhttp.status);
      }
    }
    xhttp.open("POST", "http://192.168.1.104:8083/colorshift", true);
    xhttp.send(formData);
  }, 500);
});

function sumbitOffset() {
  const token = getToken();
  const formData = new FormData();
  formData.append("token", token);
  
  
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function() {
    if (xhttp.status === 200) {
      console.log("Request successful");
      var response = xhttp.responseText;

      document.getElementById("R-input").value = "";
      document.getElementById("G-input").value = "";
      document.getElementById("B-input").value = "";

      document.getElementById("preview-image").src = response + "?" + new Date().getTime();
    }
  }
  xhttp.open("POST", "http://192.168.1.104:8083/submitOffset", true);
  xhttp.send(formData);
}