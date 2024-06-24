document.addEventListener("DOMContentLoaded", function () {
  let editBlogId;
  const blogsUrl = document.getElementById("blogs-blogs")?.getAttribute("data-url");
  const blogBaseUrl = document.getElementById("blogs-blog")?.getAttribute("data-url")?.slice(0, -1);
  const is_superuser = localStorage.getItem("is_superuser") == "true";

  if (!blogsUrl || !blogBaseUrl) {
    console.error("Required elements not found in the DOM.");
    return;
  }

  if (!is_superuser) {
    document.getElementById("add-blog").hidden = true;
  }

  console.log("blogsUrl:", blogsUrl);
  console.log("blogBaseUrl:", blogBaseUrl);

  function fetchBlogs() {
    const urlParams = new URLSearchParams(window.location.search);
    const page = urlParams.get("page") || 1;

    fetch(`${blogsUrl}?page=${page}`, {
      method: "GET",
      headers: getHeaders()
    })
      .then(response => {
        if (!response.ok) {
          // check for error response and read the error message
          if (response.status == 401) {
            alert("You are not authorized to view this page. Please login. Session expired.");
            window.location.href = "/users/login";
          }
          else {
            throw new Error("Failed to fetch blogs.");
          }
        }
        return response.json();
      })
      .then(data => {
        const blogList = document.getElementById("blogList");
        blogList.innerHTML = "";
        // data.blogs.reverse().forEach(blog => {
        data.blogs.forEach(blog => {
          // const isSuperUser = is_superuser | false; // Default to true if not specified
          // console.log('blog.image:', blog.image);
          console
          blogList.innerHTML += `
            <li class="list-group-item" data-id="${blog.id}">
              <div class="clearfix">
                ${blog.image ? `<img src="${blog.image}" class="blog-image img-fluid" alt="${blog.title}">` : `<img src="${blog.image_url}" class="blog-image img-fluid" alt="${blog.title}">`}
                <div class="blog-content">
                  <a href="${blog.news_source}" class="blog-link" target="_blank">${blog.title}</a>
                  ${is_superuser ? `<span class="edit-icon" data-toggle="modal" data-target="#editBlogModal" data-id="${blog.id}">&#9998;</span>` : ''}
                  <p>${blog.content}</p>
                </div>
              </div>
            </li>
          `;
      });

      // Add pagination links
      const pagination = document.getElementById("pagination");
      pagination.innerHTML = "";
      for (let i = 1; i <= data.pages; i++) {
        pagination.innerHTML += `<li class="page-item ${page == i ? "active" : ""}"><a class="page-link" href="/blogs?page=${i}" data-page="${i}">${i}</a></li>`;
      }
      });
  }
  // <p>${truncateContent(blog.content)}</p>


  function getHeaders() {
    return {
      Authorization: localStorage.getItem("access_token"),
      Accept: "application/json",
      "Content-Type": "application/json",
    };
  }

  function truncateContent(content) {
    return content.length > 200 ? content.substring(0, 200) + "..." : content;
  }

  function handleSubmit(url, method, title, content) {
    const formData = new FormData();
    title = document.getElementById("editTitle").value;
    content = document.getElementById("editContent").value;
    formData.append("title", title);
    formData.append("content", content);
    
    const imageFile = document.getElementById("imageFile").files[0];
    if (imageFile) {
      formData.append("image", imageFile);
    }

    fetch(url, {
      method: method,
      headers: {
        Authorization: localStorage.getItem("access_token")
      },
      body: formData,
    })
      .then(() => {
        // close bootstrap modal by id
        document.getElementById("close-modal").click();
        fetchBlogs();
      });
  }


  const addBlogButton = document.getElementById("add-blog");
  if (addBlogButton) {
    addBlogButton.addEventListener("click", function () {
      document.getElementById("editBlogModalLabel").innerText = "Add Blog";
      document.getElementById("editTitle").value = "";
      document.getElementById("editContent").value = "";
      document.getElementById("deleteblog").hidden = true;
      editBlogId = undefined;
    });
  }

  const blogForm = document.getElementById("blogForm");
  if (blogForm) {
    blogForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const title = document.getElementById("title").value;
      const content = document.getElementById("content").value;
      handleSubmit(blogsUrl, "POST", title, content);
    });
  }

// Event delegation for handling edit icon clicks
document.getElementById('blogList').addEventListener('click', function(event) {
  if (event.target.classList.contains('edit-icon')) {
      editBlogId = event.target.getAttribute('data-id');
      console.log('Edit icon clicked for blog ID:', editBlogId);

      // Make an API call to get the blog details
      fetch(`${blogBaseUrl}${editBlogId}`, {
          method: 'GET',
          headers: getHeaders(),
      })
          .then(response => response.json())
          .then(blog => {
              // Fill the form with the blog details
              document.getElementById('editTitle').value = blog.title ||'';
              document.getElementById('editContent').value = blog.content || '';
              document.getElementById('imageFile').value = null; // Clear the old file input
              document.getElementById("deleteblog").hidden = false;
              // Handle the image separately if needed
          })
          .catch(error => {
              console.error('Error fetching blog details:', error);
          });
  }
});

  const editBlogForm = document.getElementById("editBlogForm");
  if (editBlogForm) {
    editBlogForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const title = document.getElementById("editTitle").value;
      const content = document.getElementById("editContent").value;
      const method = editBlogId === undefined ? "POST" : "PATCH";
      const url = editBlogId === undefined ? blogsUrl : `${blogBaseUrl}${editBlogId}`;
      handleSubmit(url, method, title, content);
    });
  }

  const deleteBlogButton = document.getElementById("deleteblog");
  if (deleteBlogButton) {
    deleteBlogButton.addEventListener("click", function (e) {
      e.preventDefault();
      if (confirm("Are you sure you want to delete this blog?")) {
        fetch(`${blogBaseUrl}${editBlogId}`, {
          method: "DELETE",
          headers: getHeaders(),
        })
          .then(() => {
            fetchBlogs();
          });
      }
    });
  }

  // Fetch blogs on page load
  fetchBlogs();
});
