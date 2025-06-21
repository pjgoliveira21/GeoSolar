// Objeto global que abriga o mapa e todas as suas propriedades
var theMap;

// Objeto que abriga os marcadores
var markers;

// Propriedades de inicialização do mapa
const defaultLatPosition = 38.7900248;
const defaultLngPosition = -9.2021936;
const iconSize = 40;
const defaultZoom = 7;
const popupOptions = { maxWidth: 400 };

const stationIcon = { iconUrl: "../static/images/pin.png", iconSize: [iconSize, iconSize] };
const IotIcon = { iconUrl: "../static/images/iotpin.png", iconSize: [iconSize, iconSize] };

const defaultMapOptions = { center: [defaultLatPosition, defaultLngPosition], zoom: defaultZoom, maxBoundsViscosity: 0.7, minZoom: 3 };

export function initMapa() {

  // Criação do objeto mapa
  theMap = new L.map(document.getElementById("map"), defaultMapOptions);

  // Adição de camada de mapa base
  let mainMap = new L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.{ext}', {
    minZoom: 0,
    maxZoom: 20,
    attribution: '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    ext: 'png'
  });
  theMap.addLayer(mainMap);

  // Determinar os limites do mapa
  let southWest = L.latLng(85, -180);
  let northEast = L.latLng(-85, 180);
  let maxbounds = L.latLngBounds(southWest, northEast);
  theMap.setMaxBounds(maxbounds);

  // Adição de camada onde serão guardados os marcadores/estações
  markers = L.markerClusterGroup();

  // Evento para centralizar o mapa nas coordenadas do marcador clicado
  theMap.on('popupopen', function (e) {
    let targetCoords = { lat: e.popup._latlng.lat, lng: e.popup._latlng.lng }
    theMap.setView(targetCoords);
  });
}

export function moveToTarget(lat, lng) {
  // Centralizar o mapa nas coordenadas fornecidas
  theMap.setView([lat, lng], 15);
}

// Função para substituir os marcadores com novos a partir dos dados recebidos
export function setMarkers(stationData, IoTData) {

  // Limpar marcadores existentes
  theMap.removeLayer(markers)
  markers.clearLayers();

  // Por cada objeto de dados, criar um marcador
  stationData.forEach(station => {

    // Propriedades do marcador
    const marker = {
      title: station["id"],
      icon: L.icon(stationIcon),
    };

    // Criação do marcador
    let pin = new L.Marker([station["latitude"], station["longitude"]], marker);

    // Conteúdo HTML do popup, incluindo um fotografia de satélite de suas coordenadas, nome, localização, capacidade e url
    let popupContent = `
    <div class="card" style="width: 13rem;">
      <img class="img-fluid" src="${
      // Se a estação tiver o campo img definido como sat ou tiver o campo nulo, usar a API do Google Maps para obter a imagem
      // Caso contrário, usar a imagem fornecida
      station["img"] === "sat" || station["img"] === undefined
        ? `https://maps.googleapis.com/maps/api/staticmap?center=${station["latitude"]},${station["longitude"]}&zoom=18&size=400x400&maptype=satellite&key=AIzaSyBD6RsdK-8q5WIQGwkiZ6R1pfXTwiWvn2M`
        : "/static/images/stations/" + station["img"]
      }" alt="Station image">
      <div class="card-body">
        <h5 class="card-title">${station["name"]}</h5>
        <p class="card-text">${station["country"]}, ${station["continent"]}</p>
        <p class="card-text">Capacity: ${station["capacity"]} MW</p>
        ${station["img"] ? "" :
        `<a href="${station["wikiUrl"]}" class="btn btn-primary text-light">More Info</a>`
      }
        
      </div>
    </div>
    `;


    // Associar o popup ao marcador
    pin.bindPopup(popupContent, popupOptions);

    // Adicionar o marcador ao grupo de marcadores
    markers.addLayer(pin);

  });
  // Se houver dados de IoT, adicionar marcadores de IoT
  if (IoTData) {
    IoTData.forEach(iot => {
      // Propriedades do marcador de IoT
      const iotMarker = {
        title: iot["id"],
        icon: L.icon(IotIcon),
      };

      // Criação do marcador de IoT
      let iotPin = new L.Marker([iot['position']["latitude"], iot['position']["longitude"]], iotMarker);

      // Conteúdo HTML do popup para o marcador de IoT
      let iotPopupContent = `
      <div class="card" style="width: 13rem;">
        ${iot['image_url'] ? `<img class="img-fluid" src="${iot['image_url']}" alt="IoT image">` : ''}
        <div class="card-body">
          <h5 class="card-title">Dispositivo IOT</h5>
          ${Object.entries(iot).map(([key, value]) => {
        if (typeof value === 'object' && value !== null) {
          return `<p><strong>${key}:</strong></p>` +
            Object.entries(value).map(
          ([subKey, subValue]) => `<p style="margin-left:1em;"><strong>${subKey}:</strong> ${subValue}</p>`
            ).join('');
        } else {
          return `<p><strong>${key}:</strong> ${value}</p>`;
        }
          }).join('')}
        </div>
      </div>
      `;

      // Associar o popup ao marcador de IoT
      iotPin.bindPopup(iotPopupContent, popupOptions);

      // Adicionar o marcador de IoT ao grupo de marcadores
      markers.addLayer(iotPin);
    });
  }

  // No fim, adicionar o novo grupo de marcadores ao mapa
  theMap.addLayer(markers);
}