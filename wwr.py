from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="

    response = get(f"{base_url}{keyword}")

    if response.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        # "html.parser" tells Beautifulsoup to send HTML.
        jobs = soup.find_all("section", class_="jobs")
        # Find all the section that have the class of jobs.
        # class_="jobs" is keyword argument.
        for job_section in jobs:
            job_posts = job_section.find_all("li")
            job_posts.pop(-1)
            # pop method is for removing view-all list, it is located on the last of the list.
            for post in job_posts:
                anchors = post.find_all("a")
                anchor = anchors[1]
                link = anchor["href"]
                company, region = anchor.find_all(
                    "span", class_="company")
                # Shortcut
                title = anchor.find("span", class_="title")
                job_data = {
                    "link": f"https://weworkremotely.com{link}",
                    "company": company.string.replace(",", " "),
                    "location": region.string.replace(",", " "),
                    "position": title.string.replace(",", " "),
                }
                results.append(job_data)
        return results
