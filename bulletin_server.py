from bulletin_backend import app
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Debug Mode.")
    parser.add_argument("-debug", help="debug mode", action="store_true")
    args = parser.parse_args()
    app.run(debug=args.debug)