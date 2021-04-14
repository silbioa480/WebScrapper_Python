from flask import Flask, render_template, request, redirect, send_file
from so_scrapper import get_jobs as get_so_jobs
from indeed_scrapper import get_jobs as get_indeed_jobs
from exporter import save_to_file

app = Flask("WebScrapper")

db = {}

@app.route("/")
def home() :
  return render_template("home.html")

@app.route("/report")
def report() :
  word = request.args.get('word')
  if word :
    word = word.lower()
    existngJobs = db.get(word)
    if existngJobs :
      jobs = existngJobs
    else :
      so_jobs = get_so_jobs(word)
      indeed_jobs = get_indeed_jobs(word)
      jobs = so_jobs + indeed_jobs
      db[word] = jobs
  else :
    return redirect("/")
  return render_template("report.html", searchingBy=word, resultNumber=len(jobs), jobs=jobs)

@app.route("/export")
def export() :
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs :
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

app.run(host="0.0.0.0")