# micro-ecommerce
Learn how to build a Micro eCommerce Web App with Python and Serverless Postgres


## Prerequisites
- Python experience with [30 Days of Python](https://www.codingforentrepreneurs.com/courses/30-days-python-38/) or similiar
- Django experience with [Try Django](https://www.codingforentrepreneurs.com/courses/try-django-3-2/) or similiar
- Basic understanding of HTML and CSS

## Required Software
- [Python 3.10](https://www.python.org/downloads/) or newer
- [Node.js 18.15 LTS](https://nodejs.org/) or newer (For Tailwind.CSS)


## Getting Started

To install packages and run various command shortcuts, we use pip here.

_macOS/Linux Users_
```bash
python3 -m venv venv
source venv/bin/activate
venv/bin/python -m pip install pip --upgrade
venv/bin/python -m pip install -r requirements.txt
```


_Windows Users_
```powershell
c:\Python310\python.exe -m venv venv
.\venv\Scripts\activate
python -m pip install pip --upgrade
python -m pip install -r requirements.txt
```


## Building Docker Image
We should firstly install docker in our machine, you can check the official site for docker throug this link: [docker site](https://www.docker.com).

So, for building the docker image we should run:
```
docker build -f Dockerfile -t micro-ecommerce .
```
and for running this image we should run:
```
docker run --env-file .env -p 8001:8000 --name micro-ecommerce-production -it micro-ecommerce
```