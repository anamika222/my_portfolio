const params = new URLSearchParams(window.location.search);
const id = parseInt(params.get("id"));

const post = blogPosts.find(p => p.id === id);

if (post) {
  document.title = post.title;
  document.getElementById("title").innerText = post.title;
  document.getElementById("date").innerText = post.date;
  document.getElementById("content").innerHTML = post.content;

  if (post.youtube) {
    const videoId = post.youtube.split("v=")[1];
    document.getElementById("video").innerHTML = `
      <iframe class="w-full h-64 rounded"
      src="https://www.youtube.com/embed/${videoId}"
      allowfullscreen></iframe>
    `;
  }
}
