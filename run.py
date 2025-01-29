import subprocess
import time
import webbrowser

def run_flask():
    # Start the Flask app using Waitress in a separate process
    return subprocess.Popen(['waitress-serve', '--port=8000', 'app:app'], cwd='python-backend')

def run_node():
    # Start the Node.js server in a separate process
    return subprocess.Popen(['node', 'server.js'], cwd='chatbot-backend')

if __name__ == '__main__':
    try:
        # Start Flask app with Waitress
        flask_process = run_flask()
        print("Starting Flask backend with Waitress...")

        # Give Flask some time to start
        time.sleep(5)  # Adjust if Waitress takes longer to start

        # Start Node.js server
        node_process = run_node()
        print("Starting Node.js backend...")

        # Give Node.js some time to start
        time.sleep(5)  # Adjust if Node takes longer to start

        # Open the index.html file in the default web browser
        webbrowser.open('http://127.0.0.1:5000/index.html')  # Adjust URL and port as necessary
        print("Opening the frontend in the browser...")

        # Wait for both processes to complete
        flask_process.wait()
        node_process.wait()

    except KeyboardInterrupt:
        print("Interrupted! Shutting down both processes...")

    finally:
        # Terminate both processes
        flask_process.terminate()
        node_process.terminate()
        print("Processes terminated.")
