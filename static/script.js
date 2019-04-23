async function main() {


    //hook up submit button
    $('#cup-cake-form').on('submit', async (e) => {
        e.preventDefault()
        //do ajax and submit post request to endpoint
        console.log('asdf')

        let flavor = $('#flavor')
        let size = $('#size')
        let rating = $('#rating')
        let image = $('#image')

        let res = await $.ajax({
            method: "POST",
            url: `/cupcakes`,
            contentType: "application/json",
            data: JSON.stringify({
                flavor: flavor.val().toLowerCase(),
                size: size.val().toLowerCase(),
                rating: rating.val().toLowerCase(),
                image: image.val().toLowerCase()
            }),
            success: (res) => {
                cupcake = res.cupcake
                $('#cup-cake-list').prepend($(`
                <li id='c-${cupcake.id}' class="list-group-item">
                    <h1>${cupcake.flavor.charAt(0).toUpperCase() + cupcake.flavor.slice(1)}</h1>
                    <img src=${cupcake.image}>
                    <p>Rating: ${cupcake.rating}</p>
                    <p>Size: ${cupcake.size.charAt(0).toUpperCase() + cupcake.size.slice(1)}</p >
                    <button class='btn btn-danger' id=${cupcake.id}>DELETE</button>
                </li>`))
            }
        });

        flavor.val('')
        size.val('')
        rating.val('')
        image.val('')

        console.log(res)

    })

    //hook up Delete
    $('#cup-cake-list').on('click', 'button', async (e) => {
        e.preventDefault()

        //do ajax and submit post request to endpoint
        let res = await $.ajax({
            method: "DELETE",
            url: `/cupcakes/${e.target.id}`,
            success: () => {
                $(`#c-${e.target.id}`).remove()
            }
        });
        console.log(res)
    })

    $('#search-form').on('submit', async (e) => {
        e.preventDefault()

        let search_val = $(e.target).children('input').val()
        let response = await $.get({
            url: `/search`,
            data: {
                search: search_val
            },
            success: $('cup-cake-list').empty()
        })
        console.log(response)
        $('#cup-cake-list').empty()
        for (cupcake of response.cupcakes) {
            $('#cup-cake-list').prepend($(`
                <li id='c-${cupcake.id}' class="list-group-item">
                    <h1>${cupcake.flavor}</h1>
                    <img src=${cupcake.image}>
                    <p>Rating: ${cupcake.rating}</p>
                    <p>Size: ${cupcake.size}</p>
                    <button class='btn btn-danger' id=${cupcake.id}>DELETE</button>
                </li>`))
        }
    })

    // Get all cupcakes and append to page

    let response = await $.get('/cupcakes')
    console.log(response.cupcakes)

    for (cupcake of response.cupcakes) {
        $('#cup-cake-list').prepend($(`
            <li id = 'c-${cupcake.id}' class="list-group-item">
                <h1>${cupcake.flavor}</h1>
                <img src=${cupcake.image}>
                <p>Rating: ${cupcake.rating}</p>
                <p>Size: ${cupcake.size}</p>
                <button class='btn btn-danger' id=${cupcake.id}>DELETE</button>
            </li>`))
    }

}
main()
