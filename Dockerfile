FROM python:3 as base

WORKDIR ./

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

from base as test
run ["pytest", "./src"]

from base as main
CMD ["flask", "--app", "./src/main.py", "run", "--host=0.0.0.0"]