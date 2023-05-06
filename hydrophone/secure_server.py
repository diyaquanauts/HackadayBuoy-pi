import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from base64 import b64decode
from http import cookies

USERNAME = "brett"
PASSWORD = "tarpKing"
SESSION_COOKIE_NAME = "session_id"
SESSION_SECRET = "your_session_secret"  # Replace with your own secret

class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def is_authenticated(self):
        auth_header = self.headers.get("Authorization")

        if auth_header and auth_header.startswith("Basic "):
            auth_string = b64decode(auth_header[6:]).decode("utf-8")
            username, password = auth_string.split(":")

            if username == USERNAME and password == PASSWORD:
                return True

        session_cookie = self.headers.get("Cookie")
        if session_cookie:
            session_cookie = cookies.SimpleCookie(session_cookie)
            session_value = session_cookie.get(SESSION_COOKIE_NAME)
            if session_value and session_value.value == SESSION_SECRET:
                return True

        return False

    def do_GET(self):
        if self.is_authenticated():
            if not self.headers.get("Cookie"):
                self.set_session_cookie()
            return SimpleHTTPRequestHandler.do_GET(self)

        self.send_unauthorized_response()

    def set_session_cookie(self):
        session_cookie = cookies.SimpleCookie()
        session_cookie[SESSION_COOKIE_NAME] = SESSION_SECRET
        self.send_response(200)
        self.send_header("Set-Cookie", session_cookie.output(header=""))
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def send_unauthorized_response(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Authentication required"')
        self.end_headers()
        self.wfile.write(b"Unauthorized")

if __name__ == "__main__":
    os.chdir("./")
    server_address = ("0.0.0.0", 8000)
    httpd = HTTPServer(server_address, SecureHTTPRequestHandler)
    httpd.serve_forever()

