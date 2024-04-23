from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import os
import time



class WhishData:
    def __init__(self, title, artist, genre):
        self.title = title
        self.artist = artist
        self.genre = genre

    def __str__(self):
        return f"{self.title} - {self.artist} ({self.genre})"
    
    def to_dict(self):
        return {"title": self.title, "artist": self.artist, "genre": self.genre}

    
class AbstractScrapingClass:

    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = self.start_driver()

    # Método para iniciar el driver
    def start_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        options.headless = False
        service = Service(executable_path=self.driver_path)
        return webdriver.Chrome(service=service, options=options)
    
    # Método para borrar la caché
    def clear_cache(self):
        if self.driver:
            self.driver.delete_all_cookies()
            self.driver.execute_script("window.localStorage.clear();") # Limpiar 
            self.driver.execute_script("window.sessionStorage.clear();")

    # Método para iniciar sesión
    def login(self, url, username, password):
        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')  # Maximiza la ventana del navegador
        options.headless = False
       
        service = Service(executable_path=self.driver_path) # Inicializa el servicio
        self.driver = webdriver.Chrome(service=service, options=options) # Inicializa el driver
        self.driver.get(url) # Abre la página

        wait = WebDriverWait(self.driver, 5) 
        try:
            
            login_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/ul[2]/li[3]/a"))) # Busca el botón de login de la página
            login_button.click() # Hace click en el botón
            time.sleep(3)

            username_field = wait.until(EC.presence_of_element_located((By.ID, "username-field"))) # Busca el campo de usuario
            password_field = wait.until(EC.presence_of_element_located((By.ID, "password-field"))) # Busca el campo de contraseña
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))) # Busca el botón de login

            username_field.send_keys(username) # Introduce el usuario
            password_field.send_keys(password) # Introduce la contraseña
            login_button.click() # Hace click en el botón de login
            time.sleep(3)  # Espera a que cargue la página
            
            return True

        except Exception as e:
            print(f"Error durante el login: {e}") 

            return False


    def getFollowedGenres(self):
        # Aquí va el código para obtener los géneros seguidos
        genres = []
        if not self.driver:
            print("Driver buscando gatitos...")
            return genres

        wait = WebDriverWait(self.driver, 5)
        try:
            print("Obteniendo géneros seguidos...")
            # Hace click en el botón de géneros
            genres_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[1]/div[1]/div[2]/div[1]/div/ol/li[3]")))
            genres_button.click()
            time.sleep(3)
            genre= wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[1]/div[1]/div[2]/div[7]/div/div[1]/ol/li[2]")))
            genre.click()
            time.sleep(3)
            inners= wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[1]/div[1]/div[2]/div[7]/div/div[4]/div/div/ol")))
            lista_inners= inners.find_elements(By.TAG_NAME, "li")
            for inner in lista_inners:
                inn= inner.find_element(By.CLASS_NAME, "genre-info")
                inn_info =inn.find_element(By.CLASS_NAME, "genre-info-inner")
                genre= inn_info.find_element(By.CLASS_NAME, "genre-name").text             
                genres.append(genre)
  
            return genres
        except:
            return genres
        
    # Método para obtener los géneros de un enlace
    def getGenres(self, enlace): 
        genres = []
        wait = WebDriverWait(self.driver, 5)

        if not self.driver:
            print("Driver buscando gatitos...")
            return genres

        # Click en el enlace que abre una nueva pestaña
        enlace.click()
        time.sleep(3) 

        # Captura todas las identificaciones de las pestañas
        original_window = self.driver.current_window_handle
        all_windows = self.driver.window_handles

        # Cambia a la nueva pestaña
        new_window = [window for window in all_windows if window != original_window][0]
        self.driver.switch_to.window(new_window)

        # Ejecuta el scroll y espera
        self.driver.execute_script("window.scrollTo(300, document.body.scrollHeight);")
        time.sleep(3)  

        try:
            genres_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tralbum-tags"))
            )
            genres = [genre.text for genre in genres_list.find_elements(By.TAG_NAME, "a")]
        except Exception as e:
            print(f"Error obteniendo géneros: {e}")
        finally:
            # Cierra la nueva pestaña y vuelve a la original
            self.driver.close()
            self.driver.switch_to.window(original_window)

        return genres
    
    # Método para obtener la wishlist
    def getWishlist(self):

        wishlist = []
        wait= WebDriverWait(self.driver, 5)

        if not self.driver:
            print("Driver buscando gatitos...")
            wishlist_dict = ['','','']
            return wishlist_dict
        
        try:
            whislist= wait.until(EC.presence_of_element_located((By.ID, "wishlist-items"))) # Busca la wishlist
            list_items_ol = whislist.find_elements(By.TAG_NAME, "ol")
            list_items = list_items_ol[0].find_elements(By.TAG_NAME, "li")
            list_items = [item for item in list_items if item.text] 
            for item in list_items:
                title = item.find_element(By.CLASS_NAME, "collection-item-title").text
                artist = item.find_element(By.CLASS_NAME, "collection-item-artist").text
                enlace_detail = item.find_element(By.CLASS_NAME, "collection-title-details")
                enlace= enlace_detail.find_element(By.TAG_NAME, "a")
                genre = self.getGenres(enlace)
                music_data = WhishData(title, artist, genre)
                wishlist.append(music_data)
                
            wishlist_dict = [item.to_dict() for item in wishlist]

            return wishlist_dict
        
        except Exception as e:
            print(f"Error obteniendo wishlist: {e}")
            wishlist_dict = ['','','']
            return wishlist_dict

    def getLabelsArtists(self):

        labels_artists = []

        if not self.driver:
            print("Driver buscando gatitos...")
            return labels_artists

        wait = WebDriverWait(self.driver, 5)

        try:
            print("Obteniendo labels y artistas...")
            labels_artists_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[1]/div[1]/div[2]/div[1]/div/ol/li[3]")))
            labels_artists_button.click()
            time.sleep(3)
            labels_artists_list = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[1]/div[1]/div[2]/div[7]/div/div[3]/div/div/ol")))
            list_items = labels_artists_list.find_elements(By.TAG_NAME, "li")
            
            for item in list_items:
                fan_info = item.find_element(By.CLASS_NAME, "fan-info")
                fan_info_inner = fan_info.find_element(By.CLASS_NAME, "fan-info-inner")
                fan_username= fan_info_inner.find_element(By.CLASS_NAME, "fan-username").text
                print(fan_username)
                labels_artists.append(fan_username)
           
            return labels_artists

        except Exception as e:
            print(f"Error obteniendo labels y artistas: {e}")

        return labels_artists  
    
    # Método para calcular el índice de reliability
    def getReliability(self, wishlist, followed_genres):

        total_entries = len(wishlist)

        if total_entries > 0:
            # Calcular el número de entradas en la wishlist que contienen al menos uno de los followed genres
            matching_entries = 0

            for item in wishlist:
                item_genres = set(item["genre"])  # Convertir a conjunto para búsquedas más rápidas
                if item_genres.intersection(followed_genres):
                    matching_entries += 1
                
            print(matching_entries)

            # Calcular el índice de reliability
            
            reliability_index = round(float(matching_entries / total_entries if total_entries > 0 else 0),2)
            return reliability_index

        
    # Método process
    def process(self):

        json_back = []

        if not self.driver:
            print("Driver buscando gatitos...")
            return
        
        try:
            print("Procesando datos...")
            wishlist = self.getWishlist()
            time.sleep(3)
            labels_artists = self.getLabelsArtists()
            time.sleep(3)
            followed_genres = self.getFollowedGenres()
            time.sleep(3)
            reliability = self.getReliability(wishlist, followed_genres)

            # json, porque está superextendido en apis, aplicaciones, etc...
            json_back = {
                "wishlist": wishlist,
                "labels_artists": labels_artists,
                "followed_genres": followed_genres,
                "reliability": reliability
            }
            json_data = json.dumps(json_back, indent=4)

            return json_data
        
        finally:
            if self.driver:
                self.clear_cache() # Limpia la caché a ver si así deja de salir el captcha
                self.driver.quit()

def main():
    # Inicializa el scraper
    current_directory = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(current_directory, 'chromedriver')
    scraper = AbstractScrapingClass(driver_path=driver_path)
    
    # Inicia el proceso
    try:
        print("Iniciando...")
        if not scraper.login("https://bandcamp.com/", "abacotestscraping", "TEst1234$"):
            raise Exception("No se pudo iniciar sesión.")
        
        result = scraper.process()
        print(result)

        # Guardar el resultado en un archivo
        with open('bandcamp.txt', 'w') as file:
            file.write(result)
        print("Resultado guardado en bandcamp.txt")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()





