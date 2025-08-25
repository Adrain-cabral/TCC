document.addEventListener('DOMContentLoaded', () => {
    const navButtons = document.querySelectorAll('.nav-button, .footer-nav-button');
    const contentSections = document.querySelectorAll('.content-section');
    const mapButtons = document.querySelectorAll('.map-button');
    const graphButtons = document.querySelectorAll('.graph-button');
    const mapContainers = document.querySelectorAll('.map-container');
    const graphContainers = document.querySelectorAll('.graph-container');

    let activeMaps = {}; // Para armazenar instâncias de mapas Leaflet

    // Função para ocultar todas as seções de conteúdo
    const hideAllContent = () => {
        contentSections.forEach(section => {
            section.classList.add('hidden');
        });
        mapContainers.forEach(container => container.classList.add('hidden'));
        graphContainers.forEach(container => container.classList.add('hidden'));
    };

    // Função para exibir uma seção de conteúdo específica
    const showContent = (targetId) => {
        hideAllContent();
        const targetSection = document.getElementById(targetId + '-content');
        if (targetSection) {
            targetSection.classList.remove('hidden');
        }
    };

    // Inicializa os mapas Leaflet (baseado na segunda imagem)
    const initMap = (mapId, lat, lng, zoom) => {
        if (activeMaps[mapId]) {
            activeMaps[mapId].remove(); // Remove o mapa existente se já estiver inicializado
        }
        const mapElement = document.getElementById(mapId);
        if (mapElement) {
            activeMaps[mapId] = L.map(mapId).setView([lat, lng], zoom);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(activeMaps[mapId]);
        }
    };

    // Event listeners para os botões de navegação (home e rodapé)
    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.dataset.target;
            showContent(targetId);
        });
    });

    // Event listeners para os botões "Clique aqui para ver o mapa"
    mapButtons.forEach(button => {
        button.addEventListener('click', () => {
            const mapName = button.dataset.map; // 'poluicao', 'comercial', etc.
            const mapContainerId = `map-${mapName}`;
            const mapDivId = `${mapName}-map`; // ID do div onde o mapa Leaflet será renderizado
            const mapContainer = document.getElementById(mapContainerId);

            if (mapContainer) {
                // Oculta todos os mapas e gráficos de "poluicao" antes de mostrar o atual
                document.getElementById('map-poluicao').classList.add('hidden');
                document.getElementById('graph-poluicao').classList.add('hidden');

                mapContainer.classList.remove('hidden');
                // Defina coordenadas e zoom específicos para cada tipo de mapa
                // Estas são coordenadas de exemplo para São Paulo
                if (mapName === 'poluicao') {
                    initMap(mapDivId, -23.5505, -46.6333, 10); // São Paulo
                } else if (mapName === 'comercial') {
                     initMap(mapDivId, -23.5505, -46.6333, 10);
                } else if (mapName === 'refugiados') {
                     initMap(mapDivId, -23.5505, -46.6333, 10);
                } else if (mapName === 'doencas') {
                     initMap(mapDivId, -23.5505, -46.6333, 10);
                } else if (mapName === 'lazer') {
                     initMap(mapDivId, -23.5505, -46.6333, 10);
                }
                 // Invalida o tamanho do mapa para garantir que ele seja exibido corretamente
                 if (activeMaps[mapDivId]) {
                    activeMaps[mapDivId].invalidateSize();
                }
            }
        });
    });

    // Event listeners para os botões "Clique aqui para ver o grafico"
    graphButtons.forEach(button => {
        button.addEventListener('click', () => {
            const graphContainerId = 'graph-poluicao'; // Assumindo que só há um gráfico de poluição por enquanto
            const mapContainerId = 'map-poluicao';

            document.getElementById(mapContainerId).classList.add('hidden'); // Oculta o mapa
            document.getElementById(graphContainerId).classList.remove('hidden'); // Mostra o gráfico
        });
    });

    // Oculta todos os conteúdos ao carregar a página (exceto se você quiser um default)
    hideAllContent();
});