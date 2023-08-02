import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time


def gpt_engine(doma):
    openai.api_key='#'
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=[{"role": "system", "content": "fai un riassunto adatto all'utente medio di questo testo e restituiscilo formattato" + doma}], temperature=0, max_tokens=2041)
        message = response["choices"][0]["message"]
        message=str(message)
        message=json.loads(message)
        
        return message['content']
    except openai.error.RateLimitError as e:
        err="Spiacenti il servizio ora non è disponibile causa raggiungimento limite d'utilizzo."
        return err

    except openai.error.TooManyRequestsError as e:
        err="La quantità di testo data in input al modello di IA, è maggiore a quella che quest'ultimo può gestire (seguirà aggiornamento)"
        return err


def main():

        sezione=input("Inserire la serie: ")
        anno = input("Inserire l'anno: ")
        mese = input("Inserire il mese: ")
        giorno = input("Inserire il giorno: ")

        anno=int(anno)
        mese=int(mese)
        giorno=int(giorno)

        # Inizializza il driver di Selenium (assicurati di avere il driver corretto per il tuo browser installato)
        driver = webdriver.Chrome()
        if driver is None:
            err="E' stato rilevato un errore"
            return render_template("gazz.html", spiegazione=err)
        else:

            # Apre la pagina web desiderata
            driver.get("https://www.gazzettaufficiale.it/archivioCompleto")

            formato = "%d %m %Y"
            data = datetime(anno, mese, giorno)
            data_formatted = data.strftime("%d-%m-%Y")
#-----------------------------------------------------------------------------------
#FINE INSERIMENTO DATI

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
# SCELTA SEZIONE DELLA GAZZETTA

            sez_div = driver.find_element(By.ID, "elenco_hp")
            sez_divo = sez_div.find_elements(By.CLASS_NAME, "colonna_ultima")

            for index in range(len(sez_divo)):
                titolo = sez_divo[index]

  #--------------------------------SCELTA ANNO------------------------------------
                if titolo.text.lower()==sezione or titolo.text==sezione or titolo.text.upper()==sezione :
                    sez_anni=driver.find_element(By.XPATH, "//div[@class='riga_t']/..")#torno al div padre /..==/parent
                    sez_anni.find_elements(By.ID, "multi")#cerco il div successivo che desidero
                    link_anni=sez_anni.find_elements(By.TAG_NAME, "a")#carico in una lista tutti i link

                    for x in range(len(link_anni)):#itero il link presenti nel div
                        primo_click=link_anni[x]

                        if primo_click.text==str(anno):#se il link è uguale all'anno cercato, clicco
                            link_anni[x].click()
                            time.sleep(5)
                            break
                    break
        
     #-----------------------------------------------------------------------------

            link_pagina = driver.find_elements(By.TAG_NAME, "a")

            # Itera attraverso gli elementi per trovare il link desiderato
            individuato = None

            for link in link_pagina:
                lista_link = link.text

                link_pulito = lista_link[-10:]#recupero solo gli ultimi dieci elementi della lista -10 è il decimo elemento dell'array partendo dall'ultimo e : vuol dire di selezionarli tutti
                #il metodo sopra è utilizzato èerchè la stringa restituita dal driver è "sporca" quindi ho bisogno di pulirla prima di usarla

                if data_formatted==link_pulito:
                    link.click()
                    time.sleep(5)
                    break
                else:
                    print(link_pulito)



            pag_finali=driver.find_element(By.ID, "elenco_hp")
            link_finali=pag_finali.find_elements(By.TAG_NAME, "a")

            spiegazione=" "

            for link in link_finali:
                testo_pagina=None
                link.click()
                #testo_pagina = driver.page_source
                testo_pagina=driver.find_element(By.ID, "mainFrame")
                driver.switch_to.frame(testo_pagina)
                testo_pagina=driver.find_element(By.TAG_NAME, 'body').text
                testo=testo_pagina
            
            
                spiegazione=spiegazione , gpt_engine(str(testo))

                driver.back()
        
            # Chiudi il driver di Selenium
            driver.quit()

            print(spiegazione)


if __name__ == "__main__":
   main()