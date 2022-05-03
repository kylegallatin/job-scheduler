VERSION=$(cat VERSION)
docker build -t gcr.io/serene-radius-314018/python/python-base:$VERSION .
docker push gcr.io/serene-radius-314018/python/python-base:$VERSION