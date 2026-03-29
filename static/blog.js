const blogList = document.getElementById("blogList");
const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const loadMoreBtn = document.getElementById("loadMore");

let visible = 3;
let filtered = blogPosts;

function renderBlogs() {
  blogList.innerHTML = "";
  filtered.slice(0, visible).forEach(post => {
    blogList.innerHTML += `
      <div class="bg-slate-900 p-6 rounded-xl">
        <h2 class="text-xl font-bold mb-2">${post.title}</h2>
        <p class="text-slate-400 mb-4">${post.excerpt}</p>
        <a href="blog-post.html?id=${post.id}"
          class="text-teal-400 font-semibold">
          Read More →
        </a>
      </div>
    `;
  });
}

function filterBlogs() {
  const search = searchInput.value.toLowerCase();
  const category = categoryFilter.value;

  filtered = blogPosts.filter(p => {
    return (
      (category === "all" || p.category === category) &&
      p.title.toLowerCase().includes(search)
    );
  });

  visible = 3;
  renderBlogs();
}

searchInput.addEventListener("input", filterBlogs);
categoryFilter.addEventListener("change", filterBlogs);

loadMoreBtn.onclick = () => {
  visible += 3;
  renderBlogs();
};

renderBlogs();
