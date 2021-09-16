function createCupcakeHTML(cupcake) {
    // generate html <li> for the cupcake
    li = `
    <li class="m-3">
    <h5 class="card-title text-danger opacity-50"><b>${cupcake.flavor} cupcake</b></h5>
    <p class="card-text text-secondary">size: <b>${cupcake.size}</b>, rating: <b>${cupcake.rating}</b></p>
    </li>`;
    return li
}

async function createCupcakeListHTML() {
    const res = await axios.get('api/cupcakes');
    for (let cupcake of res.data.cupcakes) {
      let newCupcake = $(createCupcakeHTML(cupcake));
      $("#cupcake-list").append(newCupcake);
    }
}


$('.add-cupcake').click(createCupcake)

async function createCupcake(evt) {
    evt.preventDefault();
    const flavor = $("#flavor").val();
    const size = $("#size").val();
    const rating = $("#rating").val();
    const image = $("#image").val();
    const res = await axios.post(`/api/cupcakes`, {flavor,size,rating,image});
    let newCupcake = $(createCupcakeHTML(res.data.cupcake));
    $("#cupcake-list").append(newCupcake);
    $("#createForm").trigger("reset");
}

createCupcakeListHTML();