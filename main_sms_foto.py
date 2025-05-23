from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Lista de números para envio
numeros = [
    "5581997835416"
]

mensagem = "Olá! Esta é uma mensagem com imagem automática via WhatsApp Web."
caminho_imagem = os.path.abspath("imagem.jpeg")  # Verifique se o arquivo realmente existe

if not os.path.isfile(caminho_imagem):
    raise FileNotFoundError(f"Imagem não encontrada no caminho: {caminho_imagem}")

# Configuração do Chrome com perfil do usuário (mantém login no WhatsApp Web)
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:/Users/Robert Fernandes/AppData/Local/Google/Chrome/User Data")
options.add_argument("--profile-directory=Default")
driver = webdriver.Chrome(options=options)

# Funções utilitárias
def esperar_elemento_visivel(by, valor, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, valor)))

def esperar_elemento_clicavel(by, valor, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, valor)))

# Função principal de envio
def enviar_mensagem(numero):
    try:
        link = f"https://web.whatsapp.com/send?phone={numero}&text&app_absent=0"
        print(f"[INFO] Abrindo link: {link}")
        driver.get(link)

        print("[INFO] Aguardando botão de clipe...")
        esperar_elemento_visivel(By.XPATH, '//div[@title="Anexar"]')

        print("[INFO] Clicando no botão de clipe...")
        esperar_elemento_clicavel(By.XPATH, '//div[@title="Anexar"]').click()

        print("[INFO] Selecionando input de imagem...")
        input_img = esperar_elemento_visivel(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
        input_img.send_keys(caminho_imagem)

        print("[INFO] Aguardando área da legenda...")
        legenda = esperar_elemento_visivel(By.XPATH, '//div[@contenteditable="true" and @data-tab]')
        legenda.click()
        legenda.send_keys(mensagem)

        print("[INFO] Clicando no botão de envio...")
        botao_enviar = esperar_elemento_clicavel(By.XPATH, '//span[@data-icon="send"]')
        botao_enviar.click()

        print(f"✅ Mensagem com imagem enviada para {numero}")
        time.sleep(3)  # Pequena pausa antes de ir para o próximo

    except Exception as e:
        print(f"❌ Erro ao enviar para {numero}: {e}")

# Enviar para todos os números
for numero in numeros:
    enviar_mensagem(numero)

driver.quit()
