from bs4 import BeautifulSoup

# WEB SCRAPING LOCAL

# Utilizando open para abrir o arquivo home.html para leitura('r'), como arquivo html
with open('home.html', 'r') as html_file:
    # Atribuindo o arquivo o conteúdo para content
    content = html_file.read()
    
    # atribuindo a soup, o metodo BeautifulSoup do conteúdo de content no formato lxml
    soup = BeautifulSoup(content, 'lxml')
    
    # Imprime o código de modo agrádavel
    print(soup.prettify())
    
    # Localiza todas as tags h5 do site
    course_html_tags = soup.find_all('h5')
    
    # For para percorrer as tags h5 e imprimi-las
    for course in course_html_tags:
        print(course.text)
    
    # Localiza todos as tags div com a classe card
    course_cards = soup.find_all('div', class_ = 'card')
    
    # Percorre todos os cards
    for course in course_cards:
        
        course_name = course.h5.text # Course_name recebe o titulo h5
        course_price = course.a.text.split()[-1] # separa o texto e recebe a ultima string, referente ao preço
        
        #imprime o nome e preço do curso
        print(f'{course_name} costs {course_price}')
        

# WEB SCRAPING REAL

# Importando requests
import requests

# Texto para pedir ao usuário qual habilidade e não é familiar para que ela seja filtrada e não selecionada
print('Put some skill that you are not familiar with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

# Acessando o código do site
html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=Python&txtKeywords=Python&txtLocation=').text

# Atribuindo a soup o código do site utilizando o metodo BeautifulSoup no formato lxml
soup = BeautifulSoup(html_text, 'lxml')

# Localiza todos os trabalhos, tag li e classe clearfix job-bx wht-shd-bx
jobs = soup.find('li', class_ = 'clearfix job-bx wht-shd-bx')

# Função para navegar no site e imprimir os trabalhos disponíveis e recém-postados
def find_jobs():
    # for para percorrer trabalhos
    for job in jobs:
        # Localiza a data de publicação do trabalho como texto
        published_date= job.find('span', class_ = 'sim-posted').span.text
        # if para filtrar somente as datas few
        if 'few' in published_date:
            
            # Localiza o nome da empresa como texto sem espaços em branco
            company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ', '')
            
            # Localiza as habilidades necessárias do trabalho
            skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '')
            
            # Localiza o link para obter mais informções do trabalho
            more_info = job.header.h2.a['href']
            
            # if para imprimir somente os trabalhos que não possuem a habilidade que o usuário não possui
            if unfamiliar_skill not in skills:
                print(f"Company Name: {company_name.strip()}")
                print(f"Required Skills: {skills.strip()}")
                print(f'more info: {more_info}')
                
                print('')

# If para a criação da automatização, se o programa for executado na main.
if __name__ == '__main__':
   # Enquanto ele estiver sendo executado... 
   while True:
        find_jobs() # Função para coletar e exivir os artistas
        time = 10 # Intervalo de execução
        print(f'Waiting {time} minutes...')
        time.sleep(time + 60) # Definindo a espera pelo intervalo de execução