import csv

def save_to_file(jobs) :
  file = open("jobs.csv", encoding='utf-8-sig', mode="w")
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "link"])
  for job in jobs :
    writer.writerow(list(job.values()))
  return