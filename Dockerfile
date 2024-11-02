FROM python:3 as base

WORKDIR ./

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

from base as test
run ["pytest", "./src"]

from base as main
CMD ["python3", "./src/main.py"]