from headlessdriver import HeadlessDriver

def handler(event, context):
    query = event['query']

    headless = HeadlessDriver()
    headless.set_implicitly_wait(10)

    headless.driver.get('https://www.google.co.jp')

    search_box = headless.driver.find_element_by_name('q')
    search_box.send_keys(query)
    search_box.submit()

    stats_elem = headless.driver.find_elements_by_css_selector("#result-stats")
    search_count = stats_elem[0].text

    headless.driver.quit()

    return {"statusCode": 200, "body": {"query": query, "result": search_count}}
