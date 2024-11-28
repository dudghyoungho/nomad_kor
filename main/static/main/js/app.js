document.addEventListener("DOMContentLoaded", () => {
  const logoScreen = document.getElementById("logoScreen");
  const loginScreen = document.getElementById("loginScreen");
  const mainScreen = document.getElementById("mainScreen");

  // Initial state
  loginScreen.classList.add("hidden");
  mainScreen.classList.add("hidden");

  // Lock/unlock scroll based on current screen
  function lockScroll(lock) {
    document.body.classList.toggle("locked", lock);
  }
  lockScroll(true);

  // Logo screen click event
  logoScreen.addEventListener("click", () => {
    logoScreen.classList.add("hidden");
    loginScreen.classList.remove("hidden");
    lockScroll(true); // Lock scroll when logo screen is shown
  });

  const userList = [
    { username: "test", password: "1234" },
    { username: "admin", password: "admin" },
  ];

  // Login form event handler
  const form = document.querySelector("form");
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    // Get input values
    const username = document.getElementById("name").value.trim();
    const password = document.getElementById("password").value.trim();

    // User validation logic
    const user = userList.find(
      (user) => user.username === username && user.password === password
    );

    if (user) {
      // Login success
      alert("로그인 성공!");
      loginScreen.classList.add("hidden");
      mainScreen.classList.remove("hidden");
      lockScroll(true); // Unlock scroll when main screen is shown
    } else {
      // Login failure
      alert("아이디 혹은 비밀번호를 다시 확인해주십시오.");
    }
  });
});








const data = [
  { number: 2, content: ['백엔드 관련 질문 드립니다..'], date: '24.03.18' },
  { number: 1, content: ['UI/UX 관련 ..'], date: '24.03.17' },
];

const tableBody = document.querySelector('.nonameboard-tablebody');
data.forEach(item => {
  const row = document.createElement('button');
  row.className = 'nonameboard-tablerow';
  row.setAttribute('data-id', item.number); // data-id 추가
  row.innerHTML = `
    <span class="nonameboard-rownumber">${item.number}</span>
    <div class="nonameboard-rowcontent">
      ${item.content.map(c => `<span>${c}</span>`).join('')}
    </div>
    <span class="nonameboard-rowdate">${item.date}</span>
  `;
  tableBody.appendChild(row);
});

document.querySelectorAll('.nonameboard-tablerow').forEach(row => {
  row.addEventListener('click', () => {
    const postId = row.getAttribute('data-id'); // 데이터 ID 가져오기
    const title = row.querySelector('.nonameboard-rowcontent span').textContent; // 제목 가져오기
    const date = row.querySelector('.nonameboard-rowdate').textContent; // 날짜 가져오기
    // 상세 페이지로 제목과 날짜 전달
    window.location.href = `detail.html?id=${postId}&title=${encodeURIComponent(title)}&date=${encodeURIComponent(date)}`;
  });
});


// 상세 페이지 스크립트
const params = new URLSearchParams(window.location.search);
const postId = params.get('id');

const title = params.get('title');
const date = params.get('date');

// 제목과 날짜 렌더링
if (title && date) {
  document.getElementById('post-title').textContent = title;
  document.getElementById('post-date').textContent = `작성일: ${date}`;
}


const posts = [
  {
    id: '1',
    title: '프론트엔드와 백엔드...',
    author: '익명',
    date: '2024.11.26',
    content: '프론트엔드와 백엔드 개발에 대한 협업 내용을 담은 글입니다.'
  },
  {
    id: '2',
    title: '함께 작업하실 크리에이터 분을 찾습니다!',
    author: '닉네임',
    date: '2024.11.25',
    content: '영상 작업 및 디자인 관련 크리에이터를 찾는 내용입니다.'
  }
];

const post = posts.find(p => p.id === String(postId));

if (post) {
  document.getElementById('post-title').textContent = post.title;
  document.getElementById('post-author').textContent = `작성자: ${post.author}`;
  document.getElementById('post-date').textContent = `작성일: ${post.date}`;
  document.getElementById('post-content').innerHTML = `<p>${post.content}</p>`;
} else {
  document.querySelector('.post-detail-container').innerHTML = `
    <p>게시글을 찾을 수 없습니다. <a href="index.html">메인 페이지로 돌아가기</a></p>
  `;
}
