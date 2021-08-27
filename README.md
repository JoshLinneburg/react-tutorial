This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app) that uses Python's [Flask](https://flask.palletsprojects.com/en/2.0.x/) micro-framework as an API. 

## Getting Started

First, install the necessary Python packages to run the Flask application:
```bash
cd api
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Then, within the same terminal, run the development server for the Flask application:
```bash
flask run
```

If you already have the dependencies installed and have activated your virtual environment, you can simply:
```bash
cd /path/to/project/react-crx-tutorial/api/
flask run
```

Or you can set an environment variable and run from any directory:
```bash
export FLASK_APP=/path/to/project/react-crx-tutorial/api/flask_app
flask run
```

Then, run the development server for the React application:
```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
