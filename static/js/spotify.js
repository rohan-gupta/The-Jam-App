$(document).ready(function(){

  function checkForAuthorizationCode(){
    if (window.location.pathname == "/users/spotify/callback/") {
      getParams = new URLSearchParams(window.location.search)

      if (getParams.has("code")){
        url = "http://127.0.0.1:8000/users/spotify/callback/2/?code=" + getParams.get("code")
        window.location.replace(url)
        console.log("Code found")
      } else{
        console.log("No code found")
      }
    }
  }

  checkForAuthorizationCode()

  $('#spotifyAuthorization').click(function(e){
    e.preventDefault();
    fetch("http://127.0.0.1:8000/users/spotify/login/", {
          method: "GET",
    })
      .then(function(response){
        return response.json()
    })
      .then(function(response){
        // console.log(response.auth_endpoint);
        window.location.replace(response.auth_endpoint)
    })
  })

})
