Build and run the app
```
docker build --target main -t variant-sudoku .; docker run -p 5000:5000 variant-sudoku
```

To view the running app, in browser go to http://localhost:5000/hello

Kill the app (all containers)
```
docker kill $(docker ps -q)
```

Build and run the tests
```
docker build --target test .
```