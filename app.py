from flask import Flask, render_template, request, redirect
from short_url import shorten_url, get_long_from_short

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html")
    # must be POST
    url = request.form["url"]
    short_url = shorten_url(url)
    return render_template("result.html", short=short_url)


@app.route("/<short_url>")
def redirect_to(short_url):
    long_url = get_long_from_short(short_url)
    if not long_url:
        return render_template("main_page.html")
    return redirect(long_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

