import os
import json
import requests
from bs4 import BeautifulSoup


HEL_URLS =[
    "https://www.hel.be/",
    "https://www.hel.be/inscriptions/",
    "https://www.hel.be/implantations/",
    "https://www.hel.be/bachelier-informatique-et-systemes-orientation-technologie-de-linformatique/",
    "https://www.hel.be/bachelier-automobile-options-expertise-mecatronique-vehicules-a-energies-alternatives/",
    "https://www.hel.be/bachelier-chimie-orientation-chimie-appliquee-environnement/",
    "https://www.hel.be/bachelier-electronique-orientation-electronique-appliquee/",
    "https://www.hel.be/bachelier-energies-alternatives-et-renouvelables/",
    "https://www.hel.be/master-en-enseignement-section-1-maternelle-primaire/",
    "https://www.hel.be/bachelier-comptabilite/",
    "https://www.hel.be/bachelier-gestion-hoteliere-orientation-management/",
    "https://www.hel.be/bachelier-relations-publiques/",
    "https://www.hel.be/bachelier-sciences-administratives-et-gestion-publique/",
    

]

def get_clean_text(url):
    headers={"User-Agent":"Mozilla/5.0"}
    response=requests.get (url,headers=headers,timeout=10)
    response.raise_for_status()

    soup=BeautifulSoup(response.content,"html.parser")


    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()


    
    raw_text=soup.get_text(separator=" ", strip=True)
    return " ".join(raw_text.split())

def main():
    os.makedirs("data",exist_ok=True)

    all_pages=[]

    for url in HEL_URLS:
        print(f"Scraping:{url}")
        try:
            text=get_clean_text(url)
            all_pages.append({"url":url , "content":text})
            print(f"  OK  ({len(text)} characters)")

        except Exception as error:
            print(f"  FAILED  ({error})")


    output_path ="data/hel_content.json"
    with open(output_path,"w", encoding="utf-8")as f:
        json.dump(all_pages,f,ensure_ascii=False,indent=2)
    
    print(f"\nDone. Saved {len(all_pages)} pages to {output_path}")

if __name__ == "__main__":
    main()



    
 