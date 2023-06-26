function getToken(){
  const tokenInput = document.getElementById("token-input");
  const token = tokenInput.value;
  return token;
}

function sendAPI(url, sendFunction, answerFunction) {
  
  const data = sendFunction();

  const xhttp = new XMLHttpRequest();

  xhttp.onload = function() { answerFunction(xhttp); };
  
  xhttp.open("POST", url, true);
  xhttp.send(data);
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
        } else {
          console.error('Request failed. Error code: ' + xhttp.status);
        }
      };

      xhttp.open("POST", "http://192.168.1.104:8083/upload", true);
      xhttp.send(formData);
    };
    reader.readAsDataURL(input.files[0]);
  }
});


function invertImage() {
  sendAPI("http://192.168.1.104:8083/invertImage", 
  function(){
    const token = getToken();
    const formData = new FormData();
    formData.append("token", token);
    return formData;
  }, function(xhttp) {
    if (xhttp.status === 200) {
      console.log("File successfully uploaded to the server.");
      var response = xhttp.responseText;

      document.getElementById("preview-image").src = response + "?" + new Date().getTime();
    } else {
      console.log("Error uploading file to the server:", xhttp.status);
    }
  }
)}
  


function extendLifeTime() {
  sendAPI("http://192.168.1.104:8083/extendLifeTime",
  function() {
    const token = getToken();
    const formData = new FormData();
    formData.append("token", token);
    return formData;
  }, function(xhttp) {
    if (xhttp.status === 200) {
      console.log("Life time extended");
    }else {
      console.error('Request failed. Error code: ' + xhttp.status);
    }
  }
)}
  
window.setInterval(() => {
  extendLifeTime();
}, 60000);

let timeoutId;

const redInput = document.getElementById('R-input');
const greenInput = document.getElementById('G-input');
const blueInput = document.getElementById('B-input');

redInput.addEventListener('input', offsetRequest);
greenInput.addEventListener('input', offsetRequest);
blueInput.addEventListener('input', offsetRequest);

function offsetRequest() {
  
  clearTimeout(timeoutId);

  timeoutId = setTimeout(function() {
    sendAPI("http://192.168.1.104:8083/colorshift",
    function() {
      const redValue = redInput.value;
      const greenValue = greenInput.value;
      const blueValue = blueInput.value;
  
      const token = getToken();
  
      const formData = new FormData();
      formData.append("token", token);
      formData.append("value_R", redValue);
      formData.append("value_G", greenValue);
      formData.append("value_B", blueValue);
      return formData;
    }, function(xhttp) {
      if (xhttp.status === 200) {
        console.log('Request successful');
        var response = xhttp.responseText;

        document.getElementById("preview-image").src = response + "?" + new Date().getTime();
      } else {
        console.error('Request failed. Error code: ' + xhttp.status);
      }
    })
  }, 500);

}

function sumbitOffset() {
  sendAPI("http://192.168.1.104:8083/submitOffset",
  function() {
    const token = getToken();
    const formData = new FormData();
    formData.append("token", token);
    return formData;
  }, function(xhttp) {
    if (xhttp.status === 200) {
      console.log("Request successful");
      var response = xhttp.responseText;

      document.getElementById("R-input").value = "";
      document.getElementById("G-input").value = "";
      document.getElementById("B-input").value = "";

      document.getElementById("preview-image").src = response + "?" + new Date().getTime();
    }else {
      console.error('Request failed. Error code: ' + xhttp.status);
    }
  });
}

function undo() {
  sendAPI("http://192.168.1.104:8083/undo",
  function() {
    const token = getToken();
    const formData = new FormData();
    formData.append("token", token);
    return formData;
  }, function(xhttp) {
    if (xhttp.status === 200) {
      console.log("Request successful");
      var response = xhttp.responseText;
      document.getElementById("preview-image").src = response + "?" + new Date().getTime();
    }else {
      console.error('Request failed. Error code: ' + xhttp.status);
    }
  });
}

function redo() {
  sendAPI("http://192.168.1.104:8083/redo", 
  function() {
    const token = getToken();
    const formData = new FormData();
    formData.append("token", token);
    return formData;
  }, function(xhttp) {
    if (xhttp.status === 200) {
      console.log("Request successful");
      var response = xhttp.responseText;
      document.getElementById("preview-image").src = response + "?" + new Date().getTime();
    }else {
      console.error('Request failed. Error code: ' + xhttp.status);
    }
  });
}


document.addEventListener('keydown', function(event) {
  if (event.ctrlKey && event.key === 'z') {
    undo();
  }
});

document.addEventListener('keydown', function(event) {
  if (event.ctrlKey && event.key === 'y') {
    redo();
  }
});



const extensionInput = document.getElementById('extension-input');
extensionInput.addEventListener('input', function(event) {
  var allExtensions = [
    ".png",".jpg",".jpeg",
    ".bmp",".tiff",".tif",
    ".ico",".webp",".pbm",
    ".pgm",".ppm",".xbm",
    ".xv",".ras",".sr",
    ".tga",".pcx",".eps",
    ".ps",".psd",".tga"
  ];
  const extensionValue = extensionInput.value;
  var matches = [];
  document.getElementById("ext-input-status").textContent = "Not selected!";

  allExtensions.forEach(function(extension) {
    extension = extension.toLowerCase();
    if (extension.includes(extensionValue)) {
      matches.push(extension)
      if (extensionValue === extension) {
        document.getElementById("ext-input-status").textContent = "Saved!";
      }
    }
  });
  
  document.getElementById('available-extensions').textContent = matches.join(', ');

});