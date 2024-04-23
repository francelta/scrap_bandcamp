
<h1>Descripción del Proyecto</h1>
<p>Este proyecto utiliza Selenium para realizar scraping de datos de la página web de Bandcamp, específicamente extrayendo información de la lista de deseos (wishlist) de un usuario, los géneros musicales que sigue, y otros datos relacionados con artistas y etiquetas musicales. El propósito es analizar la alineación de los intereses musicales del usuario con su lista de deseos y proporcionar un índice de "reliability" que refleje esta alineación.</p>

<h2>Requisitos</h2>
<ul>
<li>Python 3.8+</li>
<li>Selenium WebDriver</li>
<li>ChromeDriver compatible con la versión instalada de Google Chrome</li>
</ul>

<h2>Instalación y Configuración</h2>
<h3>Dependencias</h3>
<p>Para ejecutar este script, necesitarás instalar Selenium. Esto se puede hacer a través de pip:</p>
<pre><code>pip install selenium</code></pre>

<h3>WebDriver</h3>
<p>Necesitarás descargar ChromeDriver y asegurarte de que esté actualizado según tu versión de Google Chrome. El driver debe estar en el mismo directorio que los scripts de Python o especificado correctamente en la variable <code>driver_path</code>.</p>

<a href="https://chromedriver.chromium.org/downloads"> Pincha aquí para descargar Chromedriver </a>

<h2>Estructura del Proyecto</h2>
<p>El proyecto consiste en varios componentes clave:</p>
<ul>
<li><strong>AbstractScrapingClass:</strong> Una clase que encapsula todas las funcionalidades de Selenium para interactuar con la página web, gestionar la sesión del navegador, y realizar el scraping de datos.</li>
<li><strong>WhishData:</strong> Una clase para estructurar y almacenar datos sobre cada elemento de la lista de deseos.</li>
</ul>

<h2>Decisiones Técnicas</h2>
<h3>Uso de Selenium</h3>
<p>Se eligió Selenium por su capacidad para interactuar con páginas web dinámicas, manejar sesiones de usuario y ejecutar JavaScript, lo cual es crucial para sitios complejos como Bandcamp.</p>

<h3>Manejo de la Caché</h3>
<p>Se implementaron métodos para limpiar la caché del navegador para evitar problemas de datos obsoletos y asegurar que los tests o las sesiones de scraping no se vean afectados por datos residuales.</p>

<h3>Estructura de Datos</h3>
<p>Las estructuras de datos utilizadas son:</p>
<ul>
<li><strong>WhishData:</strong> Almacena información de títulos, artistas y géneros. Se utiliza para estructurar los datos de manera que puedan ser fácilmente manipulados y accedidos.</li>
<li><strong>Diccionarios para wishlist, labels_artists, y followed_genres:</strong> Permiten un acceso y manipulación eficiente de los datos, además de ser compatibles con la conversión a JSON para posibles usos en APIs o almacenamiento.</li>
</ul>

<h3>Cálculo de Reliability</h3>
<p>El índice de reliability se calcula como la proporción de elementos en la lista de deseos que coinciden con los géneros seguidos, proporcionando una métrica cuantitativa de cuán alineados están los intereses del usuario con sus acciones de seguimiento.</p>

<h2>Problemas y Soluciones</h2>
<p>Durante el desarrollo, se enfrentaron desafíos como la gestión de CAPTCHAs y sesiones expiradas, que se manejaron mediante reintentos y sesiones de navegador limpias.</p>

<h2>Conclusión</h2>
<p>Este script proporciona una herramienta útil para análisis de datos de usuario en Bandcamp, con potencial para expandirse a otras funcionalidades como recomendaciones basadas en datos extraídos y análisis de tendencias.</p>

