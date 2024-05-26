const apiKey = '2816fe41-4647-4f8f-84b7-733b04bd95b8'
const apiUrlPopular = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_100_POPULAR_FILMS&page='
const apiUrlSearch = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword='
const apiUlDescription = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/'

async function getMovies(url) {         // функция, которая получает данные о фильме
    const resp = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            'X-API-KEY': apiKey
        }
    })
    const respData = await resp.json()
    showMovies(respData)
}

function showMovies(data) {         //функция, которая показывает список фильмов
    const moviesEl = document.querySelector('.movies')

    document.querySelector('.movies').innerHTML = ''

    data.films.forEach(movie => {
        const movieEl = document.createElement('div')
        movieEl.classList.add('movie')
        movieEl.innerHTML = `
            <div class="movie popup__link" id="${movie.filmId}">
                <div class="movie__cover-inner">
                    <img src="${movie.posterUrlPreview}" class="movie__cover" alt="${movie.nameRu}">
                    <div class="movie__cover-darkened"></div>
                </div>
                <div class="movie__info">
                    <div class="movie__title">${movie.nameRu}</div>
                    <div class="movie__category">${movie.genres.map(genre => ` ${genre.genre}`)}</div>
                    ${
                    movie.rating &&
                    `
                    <div class="movie__average movie__average-${getColor(movie.rating)}">${movie.rating}</div>
                    `
                    }
                </div>
            </div>
        `
        moviesEl.appendChild(movieEl)
        // console.log(movie.filmId)
    })
}
async function getPages(url) {      // функция, получающая даные о количестве страниц
    const resp = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            'X-API-KEY': apiKey
        }
    })
    const respData = await resp.json()
    countPages(respData)
}

function countPages(data) {     // функция, которая выводит страницы

    const btn = document.querySelector('.btns__pages')

    for(let i = 1; i <= data.pagesCount; ++i) {
        const numPage = document.createElement('div')
        numPage.classList.add('num__page') 
        numPage.innerHTML = `
            <div class="num__page">${i}</div>
        `
        btn.appendChild(numPage)
    }
}

function getColor(data) {       // получение цвета для рейтинга
    if (data >= 7) return 'green'
    else if (data < 5) return 'red'
    else return 'orange'
}

async function getDescription(url) {        // функция, которая получает подробное описание фильма
    const resp = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            'X-API-KEY': apiKey
        }
    })
    const respData = await resp.json()
    showDescription(respData)
}

function showDescription(data) {        // показываем описание в виде попап
    const popup = document.querySelector('.popup')

    document.querySelector('.popup').innerHTML = ''

    const popupBody = document.createElement('div')
    popupBody.classList.add('popup__body')
    popup.innerHTML = `
        <div class="popup__body"> 
            <div class="popup__content">
                <a class="popup__close" id="popup__close">&times;</a>
                <div class="popup__title">${data.nameRu}</div>
                <div class="popup__text">${data.description}</div>
            </div>
        </div>
    `
    
  

}

const form = document.querySelector('form')
const search = document.querySelector('.header__search')

form.addEventListener('submit', e => {      // поиск по форме
    e.preventDefault()

    const apiSearchUrl = `${apiUrlSearch}${search.value}`
    if (search.value) {
        getMovies(apiSearchUrl)
    }

    search.value = ''
})

getMovies(apiUrlPopular).then(() => {       // вызываем getMovies
    getPages(apiUrlPopular)                 //вызываем getPages

    const page = document.querySelector('.btns__pages')
    
    page.addEventListener('click', e => {           // переключение страницы при клике
        e.preventDefault()
        const { target } = e;
        const apiPageUrl = `${apiUrlPopular}${target.innerHTML}`
    
        if(target.innerHTML) {
            getMovies(apiPageUrl)
            window.scrollBy(0, -2000)
            target.classList.add('num__active')
        }
        const num = document.querySelector('.num__active')
        num.classList.remove('num__active')
    })
    
    const popupOpen = document.querySelectorAll('.popup__link')  // получаем массив div'ов с классом popup__link
    const popupClose = document.querySelector('.popup__close')
    const popup = document.querySelector('.popup')

    // for(let i = 0; i < popupOpen.length; ++i) {         // в for мы ищем элемент, на который кликнули
    //     openPopup = popupOpen[i]
    //     openPopup.addEventListener('click', e => {
    //         e.preventDefault()
    //         popup.classList.add('active')
    //         const id = e.path[2].getAttribute('id')     // берем его id
    //         console.log(id)
    //         const urlId = `${apiUlDescription}${id}` 
    //         // getDescription(urlId)                       // подаем ссылку с описанием фильма в getDescription
    //     })
    // }

    popupClose.addEventListener('click', e => {         // закрываем попап при нажатии на крестик
        popup.classList.remove('active')               
    })
})

/*
    я думаю, что попап не закрывается, потому что ассинхронная функция getDescription(urlId) 
    отправляется в очередь, а функция закрытия выполняется синхронно, т.е. сразу,
    но к моменту ее выполнения еще нечего закрывать
*/