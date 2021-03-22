from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Safari()

def collect(rating_num):
    freq = {}
    # https://codeforces.com/problemset/page/1?tags=1600-&order=BY_RATING_ASC
    driver.get("https://codeforces.com/problemset?tags="+str(rating_num)+"-&order=BY_RATING_ASC")
    lo = 1
    hi = 1
    for page_num in driver.find_element_by_class_name("pagination").find_elements_by_class_name("page-index"):
        hi = max(hi, int(page_num.get_attribute("pageindex")))

    # print("lo: " + str(lo) + " hi: " + str(hi))
    for page_num in range(1, hi+1):
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


            # needs to handle when solved count is zero or doesn't exist
            solved_count = ""
            try:
                solved_count = cols[4].find_element_by_tag_name("a").get_attribute("innerText")[2:]
            except:
                solved_count = ""

            # print(cols[0].find_element_by_tag_name("a").get_attribute("innerHTML").strip() + " " + title + " "
            #       + " ".join(tags) + " " + rating + " " )
    return freq


freq = collect(1500)
#  = {"implementation":133, "greedy":95, "math":88, "brute force": 56}
sorted_freq = sorted(freq.items(), key=lambda kv : kv[1], reverse=True)
# print(sorted_freq)
for tup in sorted_freq:
    print(tup)
driver.close()
