FROM python:3.12

RUN mkdir /Kode_ed

WORKDIR /Kode_ed

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker_file1/app.sh

EXPOSE 8000

#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]