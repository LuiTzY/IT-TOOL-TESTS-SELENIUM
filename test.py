import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

BASE_URL = "http://localhost:8000"  

@pytest.fixture(scope="module")
def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    os.makedirs("screenshots", exist_ok=True)
    yield driver
    driver.quit()

def test_login_exitoso(setup_browser):
    driver = setup_browser
    driver.get(f"{BASE_URL}/singin/")

    time.sleep(1)
    driver.find_element(By.ID, "username").send_keys("lmarte") 
    driver.find_element(By.ID, "password").send_keys("1234")    
    driver.find_element(By.ID, "loginBtn").click()

    time.sleep(2)
    driver.save_screenshot("screenshots/login_result.png")
    assert "/home" in driver.current_url or "home" in driver.page_source


def test_registro_servidor(setup_browser):
    driver = setup_browser
    driver.get(f"{BASE_URL}/servidores/nuevo/")

    time.sleep(1)
    driver.find_element(By.ID, "id_server_name").send_keys("Servidor Test con Selenium")
    driver.find_element(By.ID, "id_ip").send_keys("192.168.1.111")
    driver.find_element(By.ID, "id_server_hostname").send_keys("itla.test.local")

    driver.find_element(By.ID, "id_server_environment").send_keys("DEV")
    driver.find_element(By.ID, "id_server_status").send_keys("activo")
    driver.find_element(By.ID, "id_server_os").send_keys("Ubuntu - 20.4 LTS")
    driver.find_element(By.ID, "id_server_type").send_keys("Servidor Web")

    driver.save_screenshot("screenshots/registro_form.png")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()

    time.sleep(2)
    driver.save_screenshot("screenshots/registro_resultado.png")
    assert "Servidor" in driver.page_source or "creado" in driver.page_source


def test_eliminar_servidor(setup_browser):
    driver = setup_browser
    driver.get(f"{BASE_URL}/servidores/")

    time.sleep(2)

    try:
        eliminar_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Eliminar')]")
        eliminar_btn.click()
        time.sleep(1)

        # Confirmación de eliminación
        driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
        time.sleep(2)
        driver.save_screenshot("screenshots/eliminacion_exitosa.png")
        assert "eliminado" in driver.page_source or "/servidores" in driver.current_url
    except:
        driver.save_screenshot("screenshots/eliminacion_fallida.png")
        assert False, "No se encontró un servidor para eliminar"

