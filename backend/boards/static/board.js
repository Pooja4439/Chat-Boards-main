const boardName = window.location.pathname.split("/").pop();
const chatLog = document.getElementById("board-area");
document.getElementById("board-name").innerHTML =
  boardName.charAt(0).toUpperCase() + boardName.slice(1) + " - chat";
console.log("board.js");
function connect() {
  console.log("Connecting");
  chatSocket = new WebSocket(
    "ws://" + window.location.host + `/ws/board/${boardName}/connect`
  );

  chatSocket.onopen = function (e) {
    console.log("Successfully connected to the WebSocket.");
  };

  chatSocket.onclose = function (e) {
    setTimeout(function () {
      console.log("Reconnecting...");
      connect();
    }, 2000);
  };

  chatSocket.onmessage = function (e) {
    const newPost = JSON.parse(e.data);

    if (newPost.posts) {
      const allPosts = JSON.parse(newPost.posts);
      for (key in allPosts) {
        const postCard = document.createElement("div");
        postCard.classList.add("post-card");
        postCard.innerHTML = `
              <p class="post-id">Post ID: ${allPosts[key].id}</p>
              <p class="post-content">${allPosts[key].post_content}</p>
              <p class="post-time">${allPosts[key].post_time}</p>
          `;
        document.querySelector(".board-container").appendChild(postCard);
      }
      chatLog.scrollTop = chatLog.scrollHeight;

      return;
    }

    if (newPost.type === "chatPost") {
      const postCard = document.createElement("div");
      postCard.classList.add("post-card");
      postCard.innerHTML = `
            <p class="post-id">Post ID: ${newPost.id}</p>
            <p class="post-content">${newPost.post_content}</p>
            <p class="post-time">${newPost.post_time}</p>
        `;
      document.querySelector(".board-container").appendChild(postCard);
    } else {
      console.log(newPost);
    }

    chatLog.scrollTop = chatLog.scrollHeight;
  };

  chatSocket.onerror = function (err) {
    console.log("WebSocket encountered an error: " + err);
    console.log("Trying for now");
  };
}

let postText = document.getElementById("postText");

postText.focus();
const chatSend = document.getElementById("chatSend");
//postText.onkeyup = function (e) {
//if (e.keyCode === 13) {
//  chatSend.click();
// }
//};

function sendNewPost(event) {
  event.preventDefault();
  if (postText.value === "") {
    return;
  }
  const postData = {
    content: postText.value,
  };

  chatSocket.send(JSON.stringify(postData));
  document.getElementById("postText").value = "";
}

connect();
