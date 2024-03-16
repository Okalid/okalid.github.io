from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

contact_submissions = []

def contact_log():
    rows = ""
    for submission in contact_submissions:
        rows += (
            "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><button onclick='deleteRow(this)'>Delete</button></td></tr>".format(
                submission.get("name", "Name"),
                submission.get("email", "Email"),
                submission.get("contactMethod", "Contact Method"),
                submission.get("date", "Date"),
                submission.get("checkbox", "checkbox"),
            )
        )

    if rows == "":
        rows = "<tr><td></td><td></td><td>No submissions yet</td></tr>"

    file_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="/main.css" id="lightTheme">
        <link rel="stylesheet" type="text/css" href="/main.dark.css" id="darkTheme">
        <meta charset="UTF-8">
        <title> My contacts and Appointments </title>
    </head>
    <nav>
        <ul>
            <li><a href="/main">Main</a> </li>
            <li><a href="/testimonies">Testimonials</a></li>
            <li><a href="/contact">Contact</a></li>
            <li><a href="/admin/contactlog">Contact log</a></li>
            <li><a href="#" id="themeButton">Dark Mode</a></li>
        </ul>
    </nav>
    <body>
        <div class="page">
            <h1>Messi contacts and Appointment </h1>
            <table style="width:80%">
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Contact Method</th>
                    <th>Date</th>
                    <th>Checkbox</th>
                    <th>Delete</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    <script src="/js/main.js"></script>
    <script src="/js/table.js"></script>
    </html>
    """
    return file_content


def parse_form_data(body):
    data = urllib.parse.parse_qs(body.decode("utf8"))
    return data


def generate_contact_response(status_code, message):
    if status_code == 201:
        return f"""<!DOCTYPE html>
                    <html>
                    <head>
                        <link rel="stylesheet" type="text/css" href="/static/css/main.dark.css" id="darkTheme">
                        <link rel="stylesheet" type="text/css" href="/static/css/main.css" id="lightTheme">
                    </head>
                    <body>
                        <nav>
                            <a href="/">Home</a>
                            <a href="/contact">Contact</a>
                        </nav>
                        <h1>Contact Form Submission</h1>
                        <p>{message}</p>
                    </body>
                    <script src="/js/main.js"></script>
                    </html>"""
    elif status_code == 400:
        return f"""<!DOCTYPE html>
                <html>
                <head>
                    <link rel="stylesheet" type="text/css" href="/static/css/main.dark.css" id="darkTheme">
                    <link rel="stylesheet" type="text/css" href="/static/css/main.css" id="lightTheme">
                </head>
                <body>
                    <nav>
                        <a href="/">Home</a>
                        <a href="/contact">Contact</a>
                    </nav>
                    <h1>Contact Form Submission Error</h1>
                    <p>{message}</p>
                </body>
                <script src="/js/main.js"></script>
                </html>"""


def server_GET(url):
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path
    query = parsed_url.query
    if path == "/" or path == "/main":
        file = "static/html/mainpage.html"
        content_type = "text/html"
    elif path == "/contact":
        file = "static/html/contactform.html"
        content_type = "text/html"
    elif path == "/testimonies":
        file = "static/html/testimonies.html"
        content_type = "text/html"
    elif path == "/admin/contactlog":
        file_content = contact_log()
        return (file_content, "text/html", 200)
    elif path == "/main.css":
        file = "static/css/main.css"
        content_type = "text/css"
    elif path == "/main.dark.css":
        file = "static/css/main.dark.css"
        content_type = "text/css"
    elif path == "/images/main":
        file = "static/images/main.png"
        content_type = "image/png"
    elif path == "/js/table.js":
        file = "static/js/table.js"
        content_type = "text/javascript"
    elif path == "/js/contact.js":
        file = "static/js/contact.js"
        content_type = "text/javascript"
    elif path == "/js/main.js":
        file = "static/js/main.js"
        content_type = "text/javascript"
    else:
        file = "static/html/404.html"
        content_type = "text/html"

    try:
        with open(file, "rb") as f:
            content = f.read()
        return content, content_type, 200
    except FileNotFoundError:
        try:
            return open("static/html/404.html").read(), "text/html", 404
        except FileNotFoundError:
            return "file not found", "text/plain", 404


def server_POST(url, body):
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path
    query = parsed_url.query
    if path == "/contact":
        form_data = parse_form_data(body)

        if (
            "name" in form_data
            and "email" in form_data
            and "date" in form_data
            and "contactMethod" in form_data
            and "checkbox" in form_data
        ):
            contact_submissions.append(
                {
                    "name": form_data["name"][0],
                    "email": form_data["email"][0],
                    "date": form_data["date"][0],
                    "contactMethod": form_data["contactMethod"][0],
                    "checkbox": form_data["checkbox"][0],
                }
            )
            return (
                generate_contact_response(201, "Thank you for your submission!"),
                "text/html",
                201,
            )
        else:
            return (
                generate_contact_response(400, "Please fill in all required fields."),
                "text/html",
                400,
            )
    else:
        return open("static/html/404.html").read(), 404


def server(url, method, body):
    if method == "GET":
        return server_GET(url)
    elif method == "POST":
        return server_POST(url, body)
    else:
        return "method not supported", "text/plain", 400


# You shouldn't need to change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call the student-edited server code.
        message, content_type, status_code = server(self.path, "GET", None)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(status_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

    def do_POST(self):
        # Call the student-edited server code.
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        message, content_type, status_code = server(self.path, "POST", body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(status_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
