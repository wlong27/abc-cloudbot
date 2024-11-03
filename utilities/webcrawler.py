import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin



def web_crawl(start_url, max_pages=1):
    pages_to_crawl = [start_url]
    crawled_pages = set()
    
    while pages_to_crawl and len(crawled_pages) < max_pages:
        url = pages_to_crawl.pop(0)
        
        if url in crawled_pages:
            continue
        
        print(f"Crawling: {url}")
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Add the current page to the crawled set
            crawled_pages.add(url)
            
            # Extract all the links from the page
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                
                if full_url not in crawled_pages:
                    pages_to_crawl.append(full_url)
                    
            print(f"Found {len(pages_to_crawl)} new links.")
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            continue
    print("Crawling finished.")
    return (pages_to_crawl)
  

def web_scrape(url):
    content = ''
    json_obj= {}
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        body_content_section = soup.find(class_='body-content')
        h1_tag = body_content_section.find('h1')
        if h1_tag: 
            json_obj["name"] = h1_tag.get_text()
        
        h2_tag = body_content_section.find('h2')
        if h2_tag:
            json_obj["created_on"] = h2_tag.get_text()
            json_obj["updated_on"] = h2_tag.get_text()

        p_elements = body_content_section.find_all('p')
        for p in p_elements:

            content += p.get_text() + ' '

        json_obj["content"] = content
    except Exception as e:
        print(f'url hit error: {url} {e}')
        return ''
    return json_obj  # Limiting to 1000 characters for demo


def security_hub_web_scrape(url):
    json_obj_list = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        h2_tags = soup.findAll('h2')
        for h2 in (h2_tags):
            json_obj_list.append(loop_tag(h2, url))


    except Exception as e:
        print(f'url hit error: {url} {e}')
        return ''
    return json_obj_list  # Limiting to 1000 characters for demo



def loop_tag(h2_tag, main_url):
    json_obj= {}
   
    title = h2_tag.get_text()
    json_obj["control_id"] = h2_tag.get_text()
    json_obj["url"] = f"[{title}]({main_url}#{h2_tag.get('id')})"
    
    current_p_tag = h2_tag.find_next('p')
    json_obj["related_requirements"] = current_p_tag.get_text()
    
    current_p_tag = current_p_tag.find_next('p')
    json_obj["category"] = current_p_tag.get_text()

    current_p_tag = current_p_tag.find_next('p')
    json_obj["severity"] = current_p_tag.get_text()

    current_p_tag = current_p_tag.find_next('p')
    json_obj["resource_type"] = current_p_tag.get_text()

    current_p_tag = current_p_tag.find_next('p')
    json_obj["config_rule"] = ' '.join(current_p_tag.get_text().split())

    current_p_tag = current_p_tag.find_next('p')
    json_obj["schedule_type"] = current_p_tag.get_text()

    current_p_tag = current_p_tag.find_next('p')
    json_obj["parameters"] = current_p_tag.get_text()

    json_obj["description"] = ''
    for sibling in current_p_tag.find_next_siblings():
        if sibling.name == 'h3':
            json_obj["remediation"] = ''
            for h3_sibling in sibling.find_next_siblings():
                if h3_sibling.name == 'h2': 
                    break
                if h3_sibling.name == 'p':  
                    json_obj["remediation"] += ' '.join(h3_sibling.get_text().split())
            break
        if sibling.name == 'p':  
            json_obj["description"] += ' '.join(sibling.get_text().split())
            
    return json_obj
