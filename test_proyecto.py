import pytest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURACIÓN ---
URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
USER = "Admin"
PASS = "admin123"

# Definimos el nombre AQUI para que no de error si falla la creación
NOMBRE_USUARIO = f"UserTest{random.randint(1000,9999)}"

@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def tomar_captura(driver, nombre):
    driver.save_screenshot(f"{nombre}.png")

# --- HISTORIAS DE USUARIO ---

# Historia 1: Login Exitoso
def test_01_login_exitoso(driver):
    driver.get(URL)
    time.sleep(3) # Espera extra para carga inicial
    driver.find_element(By.NAME, "username").send_keys(USER)
    driver.find_element(By.NAME, "password").send_keys(PASS)
    tomar_captura(driver, "1_Login_Lleno")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(4)
    assert "dashboard" in driver.current_url
    tomar_captura(driver, "1_Login_Exito")

# Historia 2: Login Fallido
def test_02_login_fallido(driver):
    # Logout
    driver.find_element(By.CLASS_NAME, "oxd-userdropdown-name").click()
    driver.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(3)
    
    # Intento fallido
    driver.find_element(By.NAME, "username").send_keys(USER)
    driver.find_element(By.NAME, "password").send_keys("ERROR")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)
    
    msg = driver.find_element(By.CLASS_NAME, "oxd-alert-content-text").text
    tomar_captura(driver, "2_Login_Error")
    assert "Invalid credentials" in msg
    
    # Entrar de nuevo
    driver.find_element(By.NAME, "username").send_keys(USER)
    driver.find_element(By.NAME, "password").send_keys(PASS)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(4)

# Historia 3: Crear Usuario
def test_03_crear_usuario(driver):
    driver.find_element(By.LINK_TEXT, "Admin").click()
    time.sleep(3)
    
    # CORRECCIÓN: Usamos XPATH por texto en lugar de indice [2]
    # Busca un botón que contenga la palabra "Add"
    driver.find_element(By.XPATH, "//button[contains(., 'Add')]").click()
    time.sleep(3)
    
    # Rol: Admin (Clic en la flecha del dropdown)
    driver.find_elements(By.CLASS_NAME, "oxd-select-text--arrow")[0].click()
    time.sleep(1)
    # Selecciona la opción que dice Admin
    driver.find_element(By.XPATH, "//*[contains(text(),'Admin')]").click()
    
    # Empleado
    driver.find_element(By.XPATH, "//input[@placeholder='Type for hints...']").send_keys("a")
    time.sleep(4) # Esperamos más a que cargue la lista
    driver.find_element(By.XPATH, "//div[@role='option']").click()
    
    # Status: Enabled (Segundo dropdown)
    driver.find_elements(By.CLASS_NAME, "oxd-select-text--arrow")[1].click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[contains(text(),'Enabled')]").click()
    
    # Claves
    # Buscamos inputs de tipo password. Deben haber 2.
    inputs_pass = driver.find_elements(By.XPATH, "//input[@type='password']")
    inputs_pass[0].send_keys("Clave123!test")
    inputs_pass[1].send_keys("Clave123!test")
    
    # Usuario Nuevo
    # El input del username suele ser el que no tiene placeholder ni es password
    # Una forma segura en este form es buscar el input que está despues del label "Username"
    driver.find_element(By.XPATH, "//label[text()='Username']/../following-sibling::div//input").send_keys(NOMBRE_USUARIO)
    
    tomar_captura(driver, "3_Crear_Datos")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(8) # Damos tiempo extra para guardar
    tomar_captura(driver, "3_Crear_Fin")
    
    # Verificamos si guardó buscando el mensaje de Success o redirigiendo
    assert "viewSystemUsers" in driver.current_url

# Historia 4: Buscar Usuario
def test_04_buscar_usuario(driver):
    if "save" in driver.current_url: # Si se quedó en la pantalla de guardar, forzamos ir a Admin
         driver.find_element(By.LINK_TEXT, "Admin").click()
         
    driver.find_elements(By.TAG_NAME, "input")[1].send_keys(NOMBRE_USUARIO)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)
    
    tomar_captura(driver, "4_Busqueda")
    # Verificamos que aparezca el nombre en la tabla
    assert NOMBRE_USUARIO in driver.page_source

# Historia 5: Borrar Usuario
def test_05_borrar_usuario(driver):
    # Solo intentamos borrar si encontramos al usuario
    if NOMBRE_USUARIO in driver.page_source:
        driver.find_element(By.CLASS_NAME, "bi-trash").click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "oxd-button--label-danger").click()
        time.sleep(4)
        
        tomar_captura(driver, "5_Borrado")
        assert "Successfully Deleted" in driver.page_source or "No Records Found" in driver.page_source
    else:
        pytest.skip("No se pudo borrar porque no se encontró el usuario")