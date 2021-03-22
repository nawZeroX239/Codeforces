from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Safari()

# returns a mapping of problem tags to the number of times(frequency) it appears in a problem for a given rating
def collect(rating_num):
    # dictionary
    freq = {}

    # base url
    driver.get("https://codeforces.com/problemset?tags="+str(rating_num)+"-&order=BY_RATING_ASC")
    last = 1
    # determine the page number for last page
    for page_num in driver.find_element_by_class_name("pagination").find_elements_by_class_name("page-index"):
        last = max(last, int(page_num.get_attribute("pageindex")))

    # loads pages until it reaches the last page that contains the problems with the given rating number
    for page_num in range(1, last+1):
        url = "https://codeforces.com/problemset/page/"+str(page_num)+"?tags="+str(rating_num)+"-&order=BY_RATING_ASC"
        driver.get(url)
        # print("navigating to page: " + url)

        # table contains html table
        table = driver.find_element_by_class_name("problems")

        # extract fields from each row and column
        for row in table.find_elements_by_tag_name("tr")[1:]:
            cols = row.find_elements_by_tag_name("td")
            li = []
            for tag in cols[1].find_elements_by_tag_name("a"):
                li.append(tag.get_attribute("innerHTML").strip())
            title = li[0]
            tags = li[1:]
            for tag in tags:
                if(tag in freq):
                    freq[tag] = freq[tag] + 1
                else:
                    freq[tag] = 1

            rating = cols[3].find_element_by_class_name("ProblemRating").get_attribute("innerHTML")

            if int(rating) > rating_num:
                return freq

            # exception is thrown when the number of participants solve is empty
            solved_count = ""
            try:
                solved_count = cols[4].find_element_by_tag_name("a").get_attribute("innerText")[2:]
            except NoSuchElementException:
                solved_count = ""
            # print(cols[0].find_element_by_tag_name("a").get_attribute("innerHTML").strip() + " " + title + " "
            #       + " ".join(tags) + " " + rating + " " )
    return freq

# pass the rating number to collect method
freq = collect(1500)

# dummy value
# freq = {"implementation":133, "greedy":95, "math":88, "brute force": 56}

# sort by increasing value in a dictionary
sorted_freq = sorted(freq.items(), key=lambda kv : kv[1], reverse=True)

# prints top 10 tags with the count for each tag
for i in range(min(10, len(sorted_freq))):
    print(sorted_freq[i][0] + ' ' + str(sorted_freq[i][1]))

driver.close()
