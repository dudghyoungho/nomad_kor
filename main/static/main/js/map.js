function move_review() {
    var menu = document.getElementsByClassName("workplace-search")[0];
    menu.style.width = 500 + 'px';

    var list = document.getElementsByClassName("wp-search-result")[0];
    list.style.width = 450 + 'px';
    list.style.height = 500 + 'px';
    list.style.backgroundColor = 'rgba(' + 256 + ', ' + 256 + ', ' + 256 + ',' + 0.7 + ')';

    document.getElementsByClassName("wp-buttons")[0].style.display = 'none';

    var img = document.getElementsByClassName("wp-image")[0];
    img.style.display = 'none';


    document.getElementsByClassName("wp-reviews-list")[0].style.display = 'block';

    document.getElementsByClassName("wp-review-upload-btn")[0].style.display = 'block';


}


function move_writing() {
    document.getElementsByClassName("wp-reviews-list")[0].style.display = 'none';
    document.getElementsByClassName("wp-reviews-writingspace")[0].style.display = 'block';

    const btn = document.getElementsByClassName("wp-review-upload-btn")[0];
    btn.addEventListener('click', () => {
        upload_writing()
    });

}

function upload_writing() {
    document.getElementsByClassName("wp-reviews-writingspace")[0].style.display = 'none';

    move_review();
}

function move_star() {
    var menu = document.getElementsByClassName("workplace-search")[0];
    menu.style.width = 500 + 'px';

    var list = document.getElementsByClassName("wp-search-result")[0];
    list.style.width = 450 + 'px';
    list.style.height = 500 + 'px';
    list.style.backgroundColor = 'rgba(' + 256 + ', ' + 256 + ', ' + 256 + ',' + 0.7 + ')';

    document.getElementsByClassName("wp-buttons")[0].style.display = 'none';

    var img = document.getElementsByClassName("wp-image")[0];
    img.style.display = 'none';


    document.getElementsByClassName("wp-star-rating")[0].style.display = 'block';


}

function move_main() {
    var menu = document.getElementsByClassName("workplace-search")[0];
    menu.style.width = 350 + 'px';

    var list = document.getElementsByClassName("wp-search-result")[0];
    list.style.width = 300 + 'px';
    list.style.height = 280 + 'px';
    list.style.backgroundColor = 'rgba(' + 256 + ', ' + 256 + ', ' + 256 + ',' + 1 + ')';

    document.getElementsByClassName("wp-buttons")[0].style.display = 'block';

    var img = document.getElementsByClassName("wp-image")[0];
    img.style.display = 'block';


    document.getElementsByClassName("wp-reviews-list")[0].style.display = 'none';

    document.getElementsByClassName("wp-review-upload-btn")[0].style.display = 'none';

    document.getElementsByClassName("wp-star-rating")[0].style.display = 'none';



}
document.addEventListener('DOMContentLoaded', () => {
    navigator.geolocation.getCurrentPosition(
        position => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            fetchNearbyCafes(latitude, longitude);
            initializeMap(latitude, longitude);
        },
        error => {
            console.error('위치 정보를 가져올 수 없습니다:', error);
            alert('위치 정보를 가져올 수 없습니다.');
        }
    );
});

async function fetchNearbyCafes(latitude, longitude) {
    try {
        const response = await fetch('/cafes/nearby/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude, longitude })
        });

        if (!response.ok) {
            throw new Error('API 요청 실패');
        }

        const cafes = await response.json();
        renderCafeList(cafes);
        initializeMap(latitude, longitude, cafes); // 지도에 카페 마커 추가
    } catch (error) {
        console.error('카페 데이터를 가져오는 중 오류 발생:', error);
    }
}

function renderCafeList(cafes) {
    const resultContainer = document.querySelector('.wp-search-result');
    resultContainer.innerHTML = ''; // 기존 데이터를 초기화

    cafes.forEach(cafe => {
        const cafeItem = document.createElement('div');
        cafeItem.classList.add('wp-cafe-item');

        cafeItem.innerHTML = `
            <img class="wp-image" src="${cafe.image_url || '/static/main/assets/default.png'}" alt="${cafe.name}">
            <h3 class="wp-name">${cafe.name}</h3>
            <p class="wp-direction">${cafe.address}</p>
            <p class="wp-open">${cafe.is_open}</p>
        `;

        resultContainer.appendChild(cafeItem);
    });
}

function initializeMap(lat, lng, cafes = []) {
    const mapOptions = {
        center: new naver.maps.LatLng(lat, lng),
        zoom: 15
    };

    const map = new naver.maps.Map('map', mapOptions);

    new naver.maps.Marker({
        position: new naver.maps.LatLng(lat, lng),
        map: map,
        title: '현재 위치'
    });

    cafes.forEach(cafe => {
        const marker = new naver.maps.Marker({
            position: new naver.maps.LatLng(cafe.latitude, cafe.longitude),
            map: map,
            title: cafe.name
        });

        const infoWindow = new naver.maps.InfoWindow({
            content: `<div style="padding:10px;">${cafe.name}<br>${cafe.address}</div>`
        });

        naver.maps.Event.addListener(marker, 'click', () => {
            infoWindow.open(map, marker);
        });
    });
}