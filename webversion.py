import flask as f
import googlesearch as gs, duckduckgo_search as ds

def search_ddg(query):
	ddgs = ds.DDGS()
	return ddgs.text(query, max_results=50)

def search_google(query):
	return gs.search(term=query, advanced=True, num_results=50)

def search_res_wrapper(query):
	search_result_template = """<br><div><a href={url}>{title}</a>   {engine}<br>{description}</div>"""
	results_html = ""
	for res in search_google(query):
		results_html += search_result_template.format(url=res.url, title=res.title, description=res.description, engine="Google")
	for res in search_ddg(query):
		results_html += search_result_template.format(url=res["href"], title=res["title"], description=res["body"], engine="DuckDuckGo")
	return results_html

#host = '192.168.178.47'
host = "0.0.0.0"

app = f.Flask(__name__)

homepage_template = '''
<h2>Enter Search Query</h2>  <form method="POST"><input name="search"><input type="submit"></form>'''



@app.route('/')
def homepage():
	return homepage_template

@app.route('/', methods=["POST"])
def form_eval():
	return homepage_template + \
		f'<h3>You entered "{f.request.form["search"]}" as a search query! Results:</h3>' + \
		search_res_wrapper(f.request.form["search"])

app.run(host=host, debug=True)