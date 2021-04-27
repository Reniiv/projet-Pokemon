const pokedex = document.getElementById("pokedex");

function fetchPokemons(list) {
  const promises = [];
  for (let i = 1; i <= 102; i++) {
    promises.push(fetch(`https://pokeapi.co/api/v2/pokemon/${i}`).then(res => res.json()));
  }
  Promise.all(promises).then(results => {
    const pokemons = results.map(result => ({name: result.name, id: result.id}));
    displayPokemons(pokemons, list)
  })
}

function displayPokemons(pokemons, list) {
  pokedex.innerHTML = pokemons.map(pokemon => `<li class="card"><img id="card${pokemon.id}"  class="card-image" src="/static/cartedos.png/"><h2>${pokemon.id}</h2></li>`).join('\n');
  for (const [key, value] of list.entries()) {
    if (value == 1) setPokemonImage(key + 1, `/static/pokemon/${key + 1}_hires.png`)
  }
}

function setPokemonImage(pokemonID, imageURL) {
  const image = document.getElementById("card" + pokemonID);
  image.src = imageURL;
}