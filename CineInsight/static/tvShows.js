let isLoadingMovies = false;
let loadedMovieIds = [];
let page = 2;

$(document).ready(function () {
    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
            loadMoreTv();
        }
    });
});

function loadMoreTv() {
    if (isLoadingMovies) {
        return;
    }

    isLoadingMovies = true;

    const loadingDiv = $('#loading');
    loadingDiv.show();

    $.ajax({
        url: `/load_more_tv/${page}/`,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if (data.tv.length > 0) {
                const movieContainer = $('#movie-container');
                data.tv.forEach(movie => {
                    const movieCard = createMovieCard(movie);
                    movieContainer.append(movieCard);
                });
                page++;
            } else {
                loadingDiv.text('No more movies');
            }
        },
        complete: function () {
            loadingDiv.hide();
            isLoadingMovies = false;
        },
        error: function () {
            console.error('Failed to load more movies.');
            isLoadingMovies = false;
        }
    });
}

function createMovieCard(movie) {
    const movieCard = `
        <a href="/tvdetails/${movie.id}" style="text-decoration: none; color: black;">
        <div class="movie-card">
            <img src="https://image.tmdb.org/t/p/w500/${movie.poster_path}" alt="${movie.name} Poster">
            <div class="movie-details">
                <h2 class="movie-title">${movie.name}</h2>
                <p class="release-date">Release Date: ${movie.first_air_date}</p>
                <!-- Add other details as needed -->
            </div>
        </div>
        </a>
    `;
    return movieCard;
}