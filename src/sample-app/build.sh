# The build script should be run from the parent directory to enable common usage of the utils library
cd ..
docker build -t morshemesh/agogosml-sample-app:latest -f ./sample-app/Dockerfile .
containerId=$(docker run -d -p 5000:5000 morshemesh/agogosml-sample-app)
docker logs $containerId