from core import wsgi

if __name__ == "__main__":
    import bjoern

    bjoern.run(wsgi.application, "0.0.0.0", 8000)
